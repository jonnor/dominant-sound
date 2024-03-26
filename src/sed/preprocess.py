
import pandas
import numpy

# extract overlapped time-windows for spectrograms and labels
def compute_windows(arr : numpy.array, frames : int,
        pad_value=0.0,
        overlap=0.5,
        step=None,
        ):

    if step is None:
        step = int(frames * (1-overlap))
        
    windows = []
    index = []
        
    width, length = arr.shape
    
    for start_idx in range(0, length, step):
        end_idx = min(start_idx + frames, length)

        # create emmpty
        win = numpy.full((width, frames), pad_value, dtype=float)
        # fill with data
        win[:, 0:end_idx-start_idx] = arr[:,start_idx:end_idx]

        windows.append(win)
        index.append(start_idx)

    s = pandas.Series(windows, index=index)
    s.index.name = 'start_index'
    return s

