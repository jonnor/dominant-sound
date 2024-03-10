
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
