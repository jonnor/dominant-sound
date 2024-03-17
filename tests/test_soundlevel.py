
import numpy
import pandas
import os.path

from src.features.soundlevel import compute_soundlevel, soundlevel_for_file, compute_intermittency_ratio
from src.utils import fileutils

here = os.path.dirname(__file__)

def test_soundlevel_from_file():

    path = os.path.join(here, './data/flight-heathrow.ogg')
    df, meta = soundlevel_for_file(path)
    assert list(df.columns) == [0, 1]

    out_dir = os.path.join(here, 'out', 'test_soundlevel_from_file')
    fileutils.ensure_dir(out_dir)
    ax = df.plot(y=0)
    figure_path = os.path.join(out_dir, 'levels.png')
    ax.figure.savefig(figure_path)

    assert os.path.exists(figure_path)
    

def generate_whitenoise(duration, amp=1.0, sr=16000):
    n_samples = int(duration * sr)

    rng = numpy.random.default_rng()
    s = rng.uniform(size=n_samples) * amp
    
    return s

def test_intermittency_ratio():

    plot = False
    sr = 16000
    duration = 10.0*60.0
    event_duration = 0.25
    rng = numpy.random.default_rng()

    background_audio = generate_whitenoise(duration, amp=0.01, sr=sr)
    
    # The more events there are, the higher the intermittency ratio
    # at least until the events are so dense that they basically become the background
    results = []
    event_probabilities = [ 0.005, 0.01, 0.025, 0.10 ]
    for event_probability in event_probabilities:
        audio = background_audio.copy()
        event_audio = generate_whitenoise(event_duration, amp=0.1, sr=sr)        

        # simulate events
        n_events = 0
        for t in numpy.arange(0.0, duration, 0.50):
            roll = rng.uniform()
            if roll < event_probability:
                event_start = int(t*sr)
                audio[event_start:event_start+len(event_audio)] += event_audio
                n_events += 1

        levels = compute_soundlevel(audio, sr=sr)
        #print(levels.head())
        ir = compute_intermittency_ratio(levels.level)

        # debug plots
        if plot:
            out_dir = os.path.join(here, 'out', 'test_intermittency_ratio')
            fileutils.ensure_dir(out_dir)
            ax = levels.plot(y='level')
            ax.set_ylim(-120.0, 0.0)
            figure_path = os.path.join(out_dir, f'levels-eventp={event_probability}.png')
            ax.figure.savefig(figure_path)

        results.append(dict(events=n_events, events_p=event_probability, ir=ir))

    out = pandas.DataFrame.from_records(results)
    # check that both low intermittency and high intermittency has reasonable values
    assert out.iloc[0].ir <= 50.0
    assert out.iloc[-1].ir >= 80.0 


