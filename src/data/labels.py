
import io

import pandas

def load_audacity_labels(path : str) -> pandas.DataFrame:
    """
    Load labels from a file. Supports the Audacity label format
    """

    file = None
    with open(path, 'r') as f:
        contents = f.read()
        lines = contents.split('\n')
        lines = [ line for line in lines if not line.startswith('\\\t') ]
        contents = '\n'.join(lines)
        file = io.StringIO(contents)

    labels = pandas.read_csv(file, sep='\t', header=None,
                            names=['start', 'end', 'annotation'],
                            dtype=dict(start=float,end=float,annotation=str))

    labels = labels.sort_values('start', ascending=True)

    return labels

load_labels_file = load_audacity_labels

