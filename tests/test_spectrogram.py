
import os.path

import pandas
from matplotlib import pyplot as plt

from src.features.spectrogram import compute_mel_spectrogram, spectrogram_for_file, apply_weigthing, plot_spectrogram
from src.utils import fileutils

here = os.path.dirname(__file__)

    

def test_spectrogram_from_file():

    path = os.path.join(here, './data/flight-heathrow.ogg')
    df, meta = spectrogram_for_file(path)
    assert df.columns[0] == 50.0
    assert df.columns[-1] == 8000.0

    out_dir = os.path.join(here, 'out', 'test_spectrogram_from_file')
    fileutils.ensure_dir(out_dir)
    fig, ax = plt.subplots(1, figsize=(16, 4)) 
    plot_spectrogram(ax, df)
    figure_path = os.path.join(out_dir, 'spectrogram.png')
    ax.figure.savefig(figure_path)

    assert os.path.exists(figure_path)
    
    # apply weighting
    weighted = apply_weigthing(df)
    fig, ax = plt.subplots(1, figsize=(16, 4)) 
    plot_spectrogram(ax, weighted)
    ax.figure.savefig(os.path.join(out_dir, 'spectrogram_weighted.png'))
