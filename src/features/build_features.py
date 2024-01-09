import os
import pandas as pd
import numpy as np
from itertools import groupby
from src.features.soundlevel import soundlevel_for_file, compute_ln
from src.utils.fileutils import get_project_root, ensure_dir


ROOT = get_project_root()
data_root = os.path.join(ROOT, 'data/raw')
output_root = os.path.join(ROOT, 'data/processed')


def maestro_path(scene: str = 'city_center', file_id: str = '09'):
    audio_root = os.path.join(data_root, 'maestro_ds/development_audio')
    filename = f'{scene}_{file_id}.wav'
    return os.path.join(audio_root, scene, filename)


def tut_path(file_id: str = 'a001'):
    audio_root = os.path.join(data_root, 'tut_ds/TUT-sound-events-2017-development/audio/street')
    filename = f'{file_id}.wav'
    return os.path.join(audio_root, filename)


def get_moving_l90(decibels, frame_rate, moving_window):
    """
    Computes the rolling L90 for a given array of dB levels and moving window size (in seconds)
    """
    moving_window = frame_rate * moving_window
    values = []
    for i in range(0, (len(decibels) - moving_window)):
        start = i
        end = i + moving_window
        values.append(compute_ln(decibels[start:end], n=90))

    values = np.insert(np.asarray(values), obj=0, values=[np.nan for _ in range(moving_window // 2)])
    values = np.insert(np.asarray(values), obj=(len(decibels) - (moving_window // 2)),
                       values=[np.nan for _ in range(moving_window // 2)])
    return values


def generate_sed_timestamps(audio_path: str, moving_window: int, sed_db_thresh: int):
    """
    Takes a path to an audio file, returns a text file with timestamps for Sound Events detected over a nominated
    threshold given a rolling background level.

    Parameters
    ----------
    audio_path: Full path to an audio file.
    moving_window: Timeframe to calculate the rolling L90 "background" levels.
    sed_db_thresh: Threshold (in decibels) over which to class as a sound event.

    Returns
    -------
    Text file with the same name as the input file, saved to the "data/processed/[dataset_name]/[filename].txt" path
    """
    audio_id = audio_path.split('\\')[-1]
    # print(audio_id)

    if 'maestro_ds' in audio_path:
        dataset_name = 'maestro_ds'

    elif 'tut_ds' in audio_path:
        dataset_name = 'tut_ds'

    else:
        dataset_name = 'misc'

    ensure_dir(os.path.join(output_root, dataset_name, 'SED_timestamps'))

    output_path = os.path.join(output_root, dataset_name, 'SED_timestamps', audio_id.replace('.wav', '_SED.txt'))
    # print(output_path)

    # Compute A-weighted soundlevels for file
    df, meta = soundlevel_for_file(audio_path)

    # Determine the frame rate
    clip_duration = meta['duration']
    # print(clip_duration)
    sr = round(df.shape[0] / clip_duration)

    # Compute rolling L90 on A-weighted levels and append to df
    ln = get_moving_l90(decibels=df[0], frame_rate=sr, moving_window=moving_window)
    df['mln'] = ln

    # Compute difference between dBA and L90
    df['delta'] = df[0] - df['mln']

    # Fetch timestamps where dBA exceeds SED threshold
    results = []
    for k, g in groupby(enumerate(df['delta'] >= sed_db_thresh), key=lambda x: x[1]):
        if k:  # k is True
            g = list(g)  # for example: [(1, True), (2, True)]
            results.append([g[0][0], len(g)])

    sed_stamps = []
    for result in results:
        idx = result[0]
        steps = result[1]
        f_idx = idx + steps - 1
        # if steps >= 4:

        start = df.index[idx].total_seconds()
        stop = df.index[f_idx].total_seconds()

        sed_stamps.append((start, stop))

    seds = pd.DataFrame(sed_stamps)
    seds[3] = f'SED_{sed_db_thresh}'

    seds.to_csv(output_path, sep='\t', header=False, index=False)


if __name__ == "__main__":
    generate_sed_timestamps(audio_path=tut_path(), moving_window=10, sed_db_thresh=5)
