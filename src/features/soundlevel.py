
"""
Soundlevel computation from audio

Copyright Soundsensing AS 2023
Licensed under MIT
"""
import sys
import time
import math
import os.path
from typing import Optional

import numpy
import pandas
import acoustics
import soundfile
import structlog
import scipy.signal
from scipy.signal import zpk2tf
from scipy.signal import lfilter, bilinear


log = structlog.get_logger()

time_weightings = {
    'slow': 1000e-3,
    'fast': 125e-3,
}

# 
def time_filter_coefficients(sr : int,
        time : float = 0.125,
        method : str = 'standard-digital'
        ) -> tuple[numpy.array, numpy.array]:
    """
    Build filter for time integration

    Can for example be used to compute "fast" or "slow" soundlevels.
    """    

    # calculate filter
    if method == 'broken-pyacoustics':
        # Ref https://github.com/python-acoustics/python-acoustics/issues/210 
        b, a = zpk2tf([1.0], [1.0, time], [1.0])
        b, a = bilinear(b, a, fs=sr)
        print('WARNING: These coefficients are broken')
    elif method == 'standard-digital':
        # digital filter coefficients
        b = numpy.array([1, 0])
        a = numpy.array([
            (1 + (sr * time)),
            -sr * time
        ])
    elif method == 'standard-analog':
        # analog filter, to be followed by bilnear transform
        b = numpy.poly1d([1])
        a = numpy.poly1d([time, 1])
        b, a = bilinear(b, a, fs=sr)
    else:
        raise ValueError(f"Unknown method {method}")    

    return b, a
    
def time_integrated_levels(y : numpy.array,
        sr : int,
        time : float = 0.125,
        oversample : int = 10,
        method : str = 'standard-digital',
        ref : float = 1.0,
        db_offset : float = 0.0,
        passthrough : bool = False,
        ) -> tuple[numpy.array, numpy.array]:
    """
    Apply time integration and compute levels
    """

    b, a = time_filter_coefficients(sr=sr, time=time, method=method)

    # convert to power
    p = (y ** 2)

    # make sure filter initial matches start
    # avoids having to tune in from 0 or -inf
    zi = [ numpy.mean(p[0:int(sr*time)]) ]
    # perform filtering
    if passthrough:
        filt = p
    else:
        filt, _ = lfilter(b, a, p, zi=zi)   
    out = numpy.sqrt(filt)
    
    # Downsample in time
    step = int(sr*(time / oversample))
    steps = len(p)//step
    xx = numpy.arange(0, steps*step, step)
    out = out[xx]
    
    # convert to decibels
    out = 10*numpy.log((out / ref)+1e-30)   
    out += db_offset
    
    tt = xx / sr
    return tt, out


def compute_soundlevel(audio : numpy.array, sr : int,
        time = 'fast',
        weighting : str = 'A',
        oversample : int = 4,
        ) -> pandas.DataFrame:

    if isinstance(time, str):
        time = time_weightings[time]
    
    s = acoustics.Signal(audio, sr)

    # Apply frequency weigthing
    s = s.weigh(weighting)

    # Apply time integration
    # Convert to decibels
    times, levels = time_integrated_levels(s, sr=sr, time=time, oversample=oversample)

    df = pandas.DataFrame({
        'level': levels,
        'time': pandas.to_timedelta(times, unit='s'),
    })
    
    return df


def soundlevel_for_file(path : str,
    channels : Optional[tuple] = None,
    **kwargs) -> (pandas.DataFrame, dict):

    load_start = time.time()
    audio, sr = soundfile.read(path, samplerate=None, always_2d=True)
    load_end = time.time()

    if channels is None:
        channels = tuple(range(audio.shape[1]))

    secs = audio.shape[0]/sr
    compute_start = time.time()

    series = []
    for channel_no in channels:
        data = audio[:, channel_no]

        levels = compute_soundlevel(data, sr=sr, **kwargs)
    
        levels = levels.rename(columns={'level': channel_no})
        levels = levels.set_index('time')
        series.append(levels)

    compute_end = time.time()
    input_seconds = secs * len(channels)
    time_ratio = input_seconds / ( compute_end - load_start )

    meta = dict(
        channels=channels,
        duration=secs,
        load_time=numpy.round(load_end-load_start, 4),
        compute_time=numpy.round(compute_end-compute_start, 4),
        ratio=time_ratio,
    )

    df = pandas.concat(series, axis=1)

    return df, meta


def compute_leq(decibels : numpy.array):
    """
    Compute Leq indicators from soundlevels
    """
    e = 10**(decibels/10)
    mean = numpy.mean(e)
    return 10*numpy.log10(mean)

def compute_ln(decibels: numpy.array, n : int):
    """
    Compute LN indicators from soundlevels
    """

    assert n == int(n), 'n should be integer'
    assert n >= 0, 'n should be above 0'
    assert n <= 100, 'n should be below 100'
    q = 1.0-(n/100)
    return numpy.quantile(decibels, q)



def compute_moving_ln(array, win, ln=90):
    values = []
    for i in range(0, (len(array)-win)):
        start=i
        end=i+win
        values.append(compute_ln(array[start:end], n=ln))

    arr = numpy.full_like(array, fill_value=numpy.nan)
    arr[win:] = values
    
    return arr


def compute_background(levels : pandas.Series, window : float = 30.0, ln=90):

    # Leave just the timeseries in index
    index_names = levels.index.names
    levels = levels.copy()
    levels.name = 'level'
    levels = levels.to_frame().reset_index().set_index(index_names[-1])

    # ensure this is a time-series with index
    assert 'timedelta64' in str(levels.index.dtype), levels.index.dtype

    # check that this is a continious series
    avg_time_diff = (levels.index.max() - levels.index.min())/len(levels)
    diffs = numpy.diff(levels.level)
    window_length = math.ceil(pandas.Timedelta(seconds=window) / avg_time_diff)
    
    # compute background level
    background = compute_moving_ln(levels.level, win=window_length, ln=ln)

    levels['background'] = background

    # compute delta
    levels['delta'] = levels.level - levels.background

    # set index back to that of the input
    levels = levels.reset_index().set_index(index_names)
    
    return levels


