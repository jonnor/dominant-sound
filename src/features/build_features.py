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
        
    values = np.insert(np.asarray(values), obj=0, values=[np.nan for i in range(moving_window)])
    # values = np.insert(np.asarray(values), obj=0, values=[np.nan for _ in range(moving_window // 2)])
    # values = np.insert(np.asarray(values), obj=(len(decibels) - (moving_window // 2)),
    #                    values=[np.nan for _ in range(moving_window // 2)])
    return values


def merge_nearby_seds(sed_stamps, distance):
    """
    Takes a list of sound event tuples (start, end) and merges events which are within the specified distance.
    
    Parameters
    ----------
    sed_stamps: List of tuples with the starting and ending timestamps for a detected sound event
    distance: Sound events within this distance (seconds) will be merged into a single sound event
    """
    clean = []
    for n in range(len(sed_stamps)):
        if n == len(sed_stamps)-1:
            clean.append(sed_stamps[n])
            continue
            
        last = sed_stamps[n][1]
        next_first = sed_stamps[n+1][0]
        dist = next_first-last

        if dist > distance:
            clean.append(sed_stamps[n])

        elif dist <= distance:
            new_result = (sed_stamps[n][0], sed_stamps[n+1][1])
            clean.append(new_result)

    cleaner = []
    for i in range(len(clean)):
        if i == 0:
            cleaner.append(clean[i])
        
        else:
            if not clean[i][0] <= cleaner[-1][1]:
                cleaner.append(clean[i])
                
    return cleaner


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

    output_path = os.path.join(output_root, dataset_name, 'SED_timestamps', audio_id.replace('.wav', f'_SED_{sed_db_thresh}.txt'))
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

        # take timestamp from the frame prior to the event flag as a buffer
        if idx > 0:  # avoid negative index when starting from zero
            idx -= 1

        # for the baseline threshold, ensure consecutive frames over thresh (more than one)
        if sed_db_thresh == 5:
            if steps == 1:
                # leave the single frames as they are so we can see if they merge with a nearby event later
                f_idx = idx + steps
            
            elif steps == 2:
                # Additional frames to the front and end of the event to round it to 0.125 secs
                idx -= 1
                f_idx = idx + (steps+2)
                    
            elif steps == 3:
                # Additional frame to the front of the event to round it to 0.125 secs
                idx -= 1
                f_idx = idx + (steps+1)
                    
            else:
                f_idx = idx + steps
            
            # avoid index error for last frame
            if f_idx >= len(df.index):
                    f_idx = -1
            
            start = df.index[idx].total_seconds()
            stop = df.index[f_idx].total_seconds()
            sed_stamps.append((start, stop))
                
                
        # for larger thresholds, log all timestamps over thresh
        elif sed_db_thresh > 5:
            f_idx = idx + steps
            start = df.index[idx].total_seconds()
            stop = df.index[f_idx].total_seconds()
            sed_stamps.append((start, stop))
            
            
            
    # Only do merging below for baseline threshold       
    # Merge events with two or less frames inbetween them
    # Join sections where only one or two frames inbetween sound events (3 frames approx 0.093 secs)
    if sed_db_thresh == 5:
        inputs = sed_stamps
        outputs = []
        
        
        # loop over the timestamps until no more merges can be made
        while True:
            outputs=merge_nearby_seds(inputs, distance=0.09)

            if outputs != inputs:
                inputs = outputs

            else:
                break
            
        cleaner = outputs
        
    else:
        cleaner = sed_stamps
        
    
    # finally - drop any SED's < 0.04 seconds (ie, only one frame) for the baseline threshold
    final = []
    if sed_db_thresh == 5:
        for i in range(len(cleaner)):
            dist = cleaner[i][1] - cleaner[i][0]
            
            if dist > 0.04:
                final.append(cleaner[i])
            
            
    else:
        final = cleaner
    
    seds = pd.DataFrame(final)
    seds[2] = f'SED_{sed_db_thresh}'

    seds.to_csv(output_path, sep='\t', header=False, index=False)
    
    # return statement for debugging
    # return sed_stamps

if __name__ == "__main__":
    generate_sed_timestamps(audio_path=tut_path(), moving_window=10, sed_db_thresh=5)
