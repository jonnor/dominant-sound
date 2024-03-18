
import os

import pandas

from src.utils.fileutils import get_project_root
from src.data.labels import load_labels_file

project_root = get_project_root()

class_color_map = {
    'background': (0.95, 0.95, 0.95),
    'mixed': 'black',
    'speech': 'blue',
    'music': 'green',
    'rail_traffic': 'red',
    'road_traffic': 'orange',
    'other': 'grey',
    'biophony': 'yellow',
    'geophony': 'purple',
    'unknown': 'grey',
}


def load_datasets():

    datasets = pandas.DataFrame({
        'name': ['maestro', 'tut', 'bcn'],
    })
    datasets['annotations'] = datasets.name.apply(lambda name: os.path.join(project_root, 'data/processed/', f'{name}_ds', 'annotations/'))
    datasets = datasets.set_index('name')
    datasets.loc['bcn', 'annotations'] = os.path.join(project_root, 'data/raw/bcn')

    return datasets

def load_noise_classes():
    p = os.path.join(project_root, 'data/processed/noise_classes.csv')
    df = pandas.read_csv(p, sep=';', quotechar="'")
    df['noise'] = df.noise.fillna('other')
    df = df.set_index('original')
    return df

def load_annotations(dir, index={}):

    out = []
    for filename in os.listdir(dir):
    
        if not filename.endswith('.txt'):
            print('skipping', filename)
            continue
        annotations = load_labels_file(os.path.join(dir, filename))
        
        audio_basename = os.path.splitext(filename)[0]
        t = audio_basename.split('_annotations_')
        if len(t) == 2:
            audio_basename, annotator = t
            annotations['annotator'] = annotator

        t = audio_basename.split('_labels')
        if len(t) > 1:
            audio_basename = t[0]

        annotations['index'] = annotations.index
        annotations['clip'] = audio_basename
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


def dense_to_events(df : pandas.DataFrame,
                    category_column='label',
                    time_column='time',
                   ) -> pandas.DataFrame:
    """
    Convert a dense time-series with categories into events with start,end
    """
    df = df.copy() # avoid mutating input
    df['start'] = df[time_column]
    df['end'] = df[time_column]
    changes = df[category_column].ne(df[category_column].shift()).dropna()
    label_groups = changes.cumsum()

    out = df.groupby(label_groups).agg({'start':'min', 'end':'max', category_column:'first'}).reset_index(drop=True)

    return out

def single_track_labels(multi : pandas.DataFrame, mixed_class='mixed'):

    classes_active = multi.sum(axis=1)
    out = pandas.Series(['background']*len(multi), index=multi.index, dtype=pandas.StringDtype())

    # Simple definition of mixed: anytime there is any form of overlap in the labels
    out.loc[classes_active >= 2] = 'mixed'
    out.loc[classes_active == 1] = multi.idxmax(axis=1)
    return out


def clip_events(events,
    start_column='start',
    end_column='end',
    start=None,
    end=None):

    """
    Adjust events such that no event has start time before @start
    and no event has end time after @end
    """
    
    def clip_event(e): 
        if start is not None:
            if e[start_column] < start: 
                e[start_column] = start
        if end is not None:
            if e[end_column] > end: 
                e[end_column] = end
        return e
                
    events = events.apply(clip_event, axis=1)
    
    return events

