
import os

import pandas
import structlog

from src.utils.fileutils import get_project_root, ensure_dir_for_file
from src.utils.dataframe import flatten_dataframes
from src.data.annotations import load_dataset_annotations
from src.features.soundlevel import soundlevel_for_file
from src.features.spectrogram import spectrogram_for_file
from src.utils.dataframe import flatten_dataframes
from .audio import get_audio_path

log = structlog.get_logger()

def compute_soundlevels(audio_root, files, **kwargs):

    def audio_path(row):
        return get_audio_path(row['dataset'], row['clip'], audio_root)

    def get_soundlevels(audio_path) -> pandas.DataFrame:
        df, meta = soundlevel_for_file(audio_path, **kwargs)
        # we assume mono here
        assert len(df.columns) == 1, df.columns
        df = df.rename(columns={0: 'level'})
        return df, meta

    out = []
    for path in files.apply(audio_path, axis=1):       
        ss = get_soundlevels(path)
        log.info('compute-soundlevel', path=path, results=len(ss[0]))
        out.append(ss)

    df = pandas.DataFrame(out, index=files.index, columns=['soundlevels', 'meta'])
    out = flatten_dataframes(df.soundlevels)

    return out


def preprocess_soundlevels():
    """
    Compute and store soundlevels for the datasets
    """

    project_root = get_project_root()
    audio_root = os.path.join(project_root, 'data/raw/')
    soundlevels_dir = os.path.join(project_root, 'data/processed/soundlevels/')

    annotations = load_dataset_annotations()

    files = annotations.reset_index().set_index(['dataset', 'clip']).index.unique()
    files = files.to_frame()

    configurations = {
        'LAF': dict(mono=True, time='fast'),
        'LAS': dict(mono=True, time='slow'),
    }

    for name, config in configurations.items():
        df = compute_soundlevels(audio_root, files, **config)
        df['config'] = name
        df = df.reset_index().set_index(['config', 'dataset', 'clip', 'time'])
        out_path = os.path.join(soundlevels_dir, f'{name}.parquet')
        ensure_dir_for_file(out_path)
        df.to_parquet(out_path)
        log.info('preprocess-soundlevels-store', out=out_path, results=len(df), config=name)


def compute_spectrograms(audio_root, files, **kwargs):

    out = []
    for idx, row in files.iterrows():

        audio_path = get_audio_path(row['dataset'], row['clip'], audio_root)
        ss, _ = spectrogram_for_file(audio_path, **kwargs)
        ss.columns = [ str(c) for c in ss.columns ]

        log.info('compute-spectrogram', path=audio_path, results=len(ss))
        out.append(ss)

    #df = pandas.concat(out)
    ss = pandas.Series(out, index=files.index, name='spectrograms')
    out = flatten_dataframes(ss)
    return out

def preprocess_spectrograms():
    """
    Compute and store spectrograms for the datasets
    """

    project_root = get_project_root()
    audio_root = os.path.join(project_root, 'data/raw/')
    soundlevels_dir = os.path.join(project_root, 'data/processed/spectrograms/')

    annotations = load_dataset_annotations()

    files = annotations.reset_index().set_index(['dataset', 'clip']).index.unique()
    files = files.to_frame()

    configurations = {
        'logmels-64bands-256hop': dict(hop_length=256, n_mels=64),
    }

    for name, config in configurations.items():
        df = compute_spectrograms(audio_root, files, **config)

        df['config'] = name
        df = df.reset_index().set_index(['config', 'dataset', 'clip', 'time'])
        out_path = os.path.join(soundlevels_dir, f'{name}.parquet')
        ensure_dir_for_file(out_path)
        df.to_parquet(out_path)
        log.info('preprocess-spectrogram-store', out=out_path, results=len(df), config=name)


def main():
    preprocess_spectrograms()
    preprocess_soundlevels()


if __name__ == '__main__':
    main()
