
import os

import pandas

from src.utils.fileutils import get_project_root
from src.data.labels import load_labels_file

project_root = get_project_root()

def load_datasets():

    datasets = pandas.DataFrame({
        'name': ['maestro', 'tut'],
    })
    datasets['annotations'] = datasets.name.apply(lambda name: os.path.join(project_root, 'data/processed/', f'{name}_ds', 'annotations/'))
    datasets = datasets.set_index('name')

    return datasets

def load_annotations(dir, index={}):

    out = []
    for filename in os.listdir(dir):
    
        if not filename.endswith('.txt'):
            print('skipping', filename)
            continue
        annotations = load_labels_file(os.path.join(dir, filename))
        
        t = os.path.splitext(filename)[0].split('_annotations_')
        audio_basename, annotator = t
        
        annotations['index'] = annotations.index
        annotations['clip'] = audio_basename
        annotations['annotator'] = annotator
        for k, v in index.items():
            annotations[k] = v

        out.append(annotations)

    df = pandas.concat(out)
    #assert df.columns == ['']
    return df

def load_dataset_annotations(datasets=None):

    if datasets is None:
        datasets = load_datasets()

    dd = [ load_annotations(row.annotations, index=dict(dataset=idx)) for idx, row in datasets.iterrows() ]
    df = pandas.concat(dd).set_index(['dataset', 'clip', 'index'])
    return df


def make_continious_labels(events : pandas.DataFrame,
                           length : int,
                           time_resolution : float,
                           class_column='annotation',
                           classes : list[str] = None,
                          ) -> pandas.DataFrame:
    """
    Create a continious dense vector from sparse event labels
    
    Assumes that no annotated event means nothing occurred.
    """

    freq = pandas.Timedelta(seconds=time_resolution)

    # Determine classes
    if classes is None:
        classes = events[class_column].unique()
    
    # Create empty covering entire spectrogram
    duration = length * time_resolution
    ix = pandas.timedelta_range(start=pandas.Timedelta(seconds=0.0),
                    end=pandas.Timedelta(seconds=duration),
                    freq=freq,
                    closed='left',
    )
    ix.name = 'time'
    df = pandas.DataFrame({}, columns=classes, index=ix)
    assert len(df) == length, (len(df), length)
    df = df.fillna(0)
    
    # fill in event data
    for cls, start, end in zip(events[class_column], events['start'], events['end']):
        s = pandas.Timedelta(start, unit='s')
        e = pandas.Timedelta(end, unit='s')
       
        match = df.loc[s:e]
        df.loc[s:e, cls] = 1
    
    return df

