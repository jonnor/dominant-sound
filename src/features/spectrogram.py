
import time
import os

import pandas
import numpy
import librosa
import soundfile

def compute_mel_spectrogram(audio, sr,
        n_mels=64,
        fmin=50.0,
        fmax=8000.0,
        hop_length=256,
        n_fft=None,
        ref=0.0,
        htk=False,
        ) -> pandas.DataFrame:
    """
    Compute decibel-scaled mel spectrogram
    """

    if n_fft is None:
        n_fft = int(hop_length * 2)

    S = librosa.feature.melspectrogram(y=audio, sr=sr,
        n_mels=n_mels, fmin=fmin, fmax=fmax,
        hop_length=hop_length, n_fft=n_fft,
        htk=htk,
    )
    S_db = librosa.power_to_db(S, ref=ref)

    timestep = pandas.Timedelta(seconds=hop_length/sr)

    bands = librosa.mel_frequencies(n_mels=n_mels, fmin=fmin, fmax=fmax, htk=htk).round(0)
    times = pandas.Series(timestep * numpy.arange(0, len(S_db.T)), name='time')

    df = pandas.DataFrame(S_db.T, columns=bands, index=times)

    return df

def spectrogram_for_file(path : str,
    sr : int = 16000,
    **kwargs) -> (pandas.DataFrame, dict):

    load_start = time.time()
    audio, sr = librosa.load(path, sr=sr)
    load_end = time.time()

    secs = audio.shape[0]/sr
    compute_start = time.time()

    df = compute_mel_spectrogram(audio, sr=sr, **kwargs)

    compute_end = time.time()
    channels = (1,)
    input_seconds = secs * len(channels)
    time_ratio = input_seconds / ( compute_end - load_start )

    meta = dict(
        duration=secs,
        load_time=numpy.round(load_end-load_start, 4),
        compute_time=numpy.round(compute_end-compute_start, 4),
        ratio=time_ratio,
    )

    return df, meta


def apply_weigthing(spectrogram: pandas.DataFrame, frequencies = None, kind = 'A'):
    """
    NOTE: spectrogram should be decibel/log10 scaled. Not power or magnitude
    """

    if frequencies is None:
        frequencies = spectrogram.columns

    # compute weights
    weighting = librosa.frequency_weighting(frequencies, kind=kind)

    out = spectrogram.copy()    
    # apply to each band
    for w, c in zip(weighting, out.columns):
        out[c] = out[c] + w

    return out

def plot_spectrogram(ax, spectrogram : pandas.DataFrame, sr=16000):

    hop = numpy.diff(spectrogram.index)[1]
    hop_length = int((hop / pandas.Timedelta(seconds=1)) * sr)

    import librosa.display

    fmin = spectrogram.columns[0]
    fmax = spectrogram.columns[-1]
    n_mels = len(spectrogram.columns)
    librosa.display.specshow(spectrogram.values.T, ax=ax,
        fmin=fmin, fmax=fmax, y_axis='mel',
        x_axis='time', hop_length=hop_length, sr=sr,
    )
