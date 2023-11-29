
import os.path

from src.features.soundlevel import compute_soundlevel, soundlevel_for_file
from src.utils import fileutils

here = os.path.dirname(__file__)

def test_soundlevel_from_file():

    path = os.path.join(here, './data/flight-heathrow.ogg')
    df, meta = soundlevel_for_file(path)
    assert list(df.columns) == [0, 1]

    out_dir = os.path.join(here, 'out', 'test_soundlevel_from_file')
    fileutils.ensure_dir(out_dir)
    ax = df.plot(y=0)
    ax.figure.savefig(os.path.join(out_dir, 'levels.png'))

    assert False
