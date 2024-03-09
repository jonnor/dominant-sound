
import copy

import pandas
import numpy


def merge_overlapped_predictions(window_predictions, window_hop, time_resolution):
    
    # flatten the predictions from overlapped windows
    predictions = []
    for win_no, win_pred in enumerate(window_predictions):
        win_start = window_hop * win_no
        for frame_no, p in enumerate(win_pred):
            s = {
                'frame': win_start + frame_no,
                'probability': p,
            }
        
            predictions.append(s)
        
    df = pandas.DataFrame.from_records(predictions)
    df['time'] = pandas.to_timedelta(df['frame'] * time_resolution, unit='s')
    df = df.drop(columns=['frame'])
    
    # merge predictions from multiple windows 
    out = df.groupby('time').median()
    return out


def events_from_predictions(pred, threshold=0.5, label='yes', event_duration_max=1.0):
    """
    Discretize predictions into events
    """
    
    event_duration_max = pandas.Timedelta(event_duration_max, unit='s')
    
    events = []
    inside_event = False
    event = {
        'start': None,
        'end': None,
    }
    
    for t, r in pred.iterrows():
        p = r['probability']

        # basic state machine for producing events
        if not inside_event and p > threshold:
            event['start'] = t
            inside_event = True
            
        elif inside_event and ((p < threshold) or ((t - event['start']) > event_duration_max)):
            event['end'] = t
            events.append(copy.copy(event))
            
            inside_event = False
            event['start'] = None
            event['end'] = None
        else:
            pass
    
    if len(events):
        df = pandas.DataFrame.from_records(events)
    else:
        df = pandas.DataFrame([], columns=['start', 'end'], dtype='timedelta64[ns]')
    df['label'] = label
    return df


def to_sed_eval_events(e, label='label', end='end', start='start'):
    """
    Convert event lists to format expected by sed_eval
    """
    import dcase_util
    
    sed = e.copy()
    sed = e.rename(columns={
        label: 'event_label',
        end: 'event_offset',
        start: 'event_onset',
        #'file': 'source',
    })
    #print(sed)
    c = dcase_util.containers.MetaDataContainer(sed.to_dict(orient='records'))
    return c
    
def evaluate_events(ref, pred, threshold=0.5, tolerance=0.100):
    
    import sed_eval

    # Convert to sed_eval formats
    ref = to_sed_eval_events(ref, label='event')

    estimated = events_from_predictions(pred, threshold=threshold)
    estimated['start'] = estimated['start'].dt.total_seconds()
    estimated['end'] = estimated['end'].dt.total_seconds()
    est = to_sed_eval_events(estimated)

    # Compute metrics 
    metrics = sed_eval.sound_event.EventBasedMetrics(
        evaluate_onset=True,
        evaluate_offset=False, # only onsets
        event_label_list=ref.unique_event_labels,
        t_collar=tolerance,
        percentage_of_length=1.0,
    )
    metrics.evaluate(
        reference_event_list=ref,
        estimated_event_list=est,
    )
    
    # Extract metrics as flat series
    m = metrics.results_overall_metrics()
    s = pandas.Series({
      'f_measure': m['f_measure']['f_measure'],
      'precision': m['f_measure']['precision'],
      'recall': m['f_measure']['recall'],
      'error_rate': m['error_rate']['error_rate'],
      'substitution_rate': m['error_rate']['substitution_rate'],
      'deletion_rate': m['error_rate']['deletion_rate'],
      'insertion_rate': m['error_rate']['insertion_rate'],
    })
    
    return s


def compute_pr_curve(annotations, pred, thresholds=50, tolerance=0.1):

    df = pandas.DataFrame({
        'threshold': numpy.linspace(0.0, 1.0, thresholds),
    })

    metrics = df.threshold.apply(lambda t: evaluate_events(annotations, pred, threshold=t, tolerance=tolerance))
    df = pandas.merge(df, metrics, right_index=True, left_index=True)
    
    return df
