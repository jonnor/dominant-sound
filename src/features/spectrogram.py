
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

    if n_fft is None:
        n_fft = int(hop_length * 2)

    S = librosa.feature.melspectrogram(y=audio, sr=sr,
        n_mels=n_mels, fmin=fmin, fmax=fmax,
        hop_length=hop_length, n_fft=n_fft,
        htk=htk,
    )
    S_db = librosa.power_to_db(S, ref=ref)

    timestep = pandas.Timedelta(seconds=sr/hop_length)

    bands = librosa.mel_frequencies(n_mels=n_mels, fmin=fmin, fmax=fmax, htk=htk).round(0)
    times = timestep * numpy.arange(0, len(S.T))

    df = pandas.DataFrame(S_db.T, columns=bands, index=times)

    return df

def spectrogram_for_file(path : str,
    mono : bool = True,
    **kwargs) -> (pandas.DataFrame, dict):

    assert mono == True, "only mono supported"

    load_start = time.time()
    audio, sr = soundfile.read(path, samplerate=None, always_2d=True)
    load_end = time.time()

    if mono:
        audio = numpy.mean(audio, axis=1, keepdims=False)

    secs = audio.shape[0]/sr
    compute_start = time.time()

    print('start')
    df = compute_mel_spectrogram(audio, sr=sr, **kwargs)
    print('end')

    compute_end = time.time()
    channels = (1,)
    input_seconds = secs * len(channels)
    time_ratio = input_seconds / ( compute_end - load_start )

    meta = dict(
        #channels=channels,
        duration=secs,
        load_time=numpy.round(load_end-load_start, 4),
        compute_time=numpy.round(compute_end-compute_start, 4),
        ratio=time_ratio,
    )

    return df, meta
