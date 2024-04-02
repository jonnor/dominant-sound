
from src.utils.fileutils import get_project_root
from src.data.annotations import \
    load_noise_classes, load_dataset_annotations,\
    count_events_in_period, make_multitrack_labels, make_continious_labels
from src.sed.preprocess import compute_windows

import os
import math

import numpy
import pandas
import tensorflow.keras
import keras

def weighted_binary_crossentropy(zero_weight, one_weight):
    """
    Loss with support for specifying class weights
    """
    import tensorflow.keras.backend as K
    
    def weighted_binary_crossentropy(y_true, y_pred):

        # standard cross entropy
        b_ce = K.binary_crossentropy(y_true, y_pred)

        # apply weighting
        weight_vector = y_true * one_weight + (1 - y_true) * zero_weight
        weighted_b_ce = weight_vector * b_ce

        return K.mean(weighted_b_ce)

    return weighted_binary_crossentropy

def compute_class_weights(y_train):
    from sklearn.utils import class_weight
    y_train = numpy.squeeze(y_train).astype(int)
    y_train = numpy.any(y_train, axis=1)
    w = class_weight.compute_class_weight('balanced', classes=numpy.unique(y_train), y=y_train)
    #w_dict = dict(zip(numpy.unique(y_train), w))
    return w


def build_model(input_shape, dropout=0.5, lr=0.01, class_weights=None, name='sedgru', n_classes=1):

    from .models import build_sedgru, build_sednet
    
    # Model
    if name == 'sednet':
        model = build_sednet(input_shape, n_classes=n_classes,
                         filters=10,
                         cnn_pooling=[2, 2, 2],
                         cnn_temporal_pooling=2,
                         rnn_units=[5, 5],
                         dense_units=[16],
                         dropout=dropout,
                        )
    elif name == 'sedgru':
        model = build_sedgru(input_shape, n_classes=n_classes,
                             reduction_units=(16, 8),
                             rnn_units=[8, 8],
                             dense_units=[16, 8],
                             dropout=dropout)
    else:
        raise ValueError('')
        
    # Metrics
    pr_auc = tensorflow.keras.metrics.AUC(num_thresholds=200, curve="PR", name='pr_auc')
    precision = tensorflow.keras.metrics.Precision(name='precision')
    recall = tensorflow.keras.metrics.Recall(name='recall')
    
    # Loss
    if class_weights is None:
        loss = tensorflow.keras.losses.BinaryCrossentropy()
    else:
        loss = weighted_binary_crossentropy(*class_weights)
       
    model.compile(optimizer=tensorflow.keras.optimizers.Adam(learning_rate=lr),
                  loss=loss,
                  metrics=[pr_auc, precision, recall],
    )
    return model

def plot_history(history):
    from matplotlib import pyplot as plt
    
    fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
    history.index.name = 'epoch'
    history.plot(ax=axs[0], y=['loss', 'val_loss'])
    history.plot(ax=axs[1], y=['pr_auc', 'val_pr_auc'])
    axs[1].set_ylim(0, 1.0)
    axs[1].axhline(0.40, ls='--', color='black', alpha=0.5)
    
    axs[0].axhline(0.10, ls='--', color='black', alpha=0.5)
    axs[0].set_ylim(0, 1.0)

    return fig

# How often are events within N seconds of eachother. Inside the same N second window
def count_events_in_window(annotations : pandas.DataFrame,
        window='1s',
        time_resolution = 0.050,
        column='noise_class',
        ) -> pandas.DataFrame:

    e = annotations.copy()
    e['same_class'] = 'event'
    e['event_name'] = e.index
    multi = count_events_in_period(e, class_column=column, time_resolution=time_resolution)
    counts = multi.groupby(pandas.Grouper(freq=window)).mean()

    return counts

def annotation_to_windows(annotations,
        window : pandas.Timedelta,
        class_column='annotation'):

    by_clip = annotations.groupby(['dataset', 'clip'])
    out = by_clip.apply(count_events_in_window, window=window, column=class_column)

    return out


def label_windows(windows):

    df = windows.copy()

    co_occuring = df.apply(lambda s: s>0.0).sum(axis=1) > 1.0
    has_annotation = df.apply(lambda s: s>0.0).sum(axis=1) > 0.0
    df.loc[(~co_occuring & has_annotation), 'annotations'] = 'single'
    df.loc[co_occuring, 'annotations'] = 'multiple'
    df.loc[df['annotations'].isna(), 'annotations'] = 'none'

    # label single events based the one present
    df.loc[df['annotations'] == 'single', 'label'] = df.idxmax(axis=1, numeric_only=True)
    df.loc[df['annotations'] == 'none', 'label'] = 'none'
    df.loc[df['annotations'] == 'multiple', 'label'] = 'multiple'

    assert len(df) == len(windows)
    return df

def train_eval_windows(windows, target='label', group='clip'):

    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.decomposition import PCA
    from sklearn.pipeline import make_pipeline

    from sklearn.model_selection import cross_validate, GroupShuffleSplit


    estimator = make_pipeline(
        #PCA(n_components=100),
        LogisticRegression(max_iter=1000),
        #KNeighborsClassifier(n_neighbors=10),
        #RandomForestClassifier(n_estimators=100, max_depth=10),
    )

    features = [ c for c in windows.columns if c.startswith('emb.e') ]
    assert len(features) >= 1, features
    X = windows[features]
    Y = windows[target]
    groups = windows[group]

    with_na_label = Y[Y.isna()]
    assert len(with_na_label) == 0, with_na_label

    n_classes = Y.nunique()
    assert n_classes >= 1, n_classes 
    assert len(X) == len(Y)

    splitter = GroupShuffleSplit(test_size=1, n_splits=3)
    results = cross_validate(estimator, X=X, y=Y,
        groups=groups,
        cv=splitter,
        error_score='raise',
        scoring='f1_macro',
        verbose=2,
        #return_estimator=True,
        return_train_score=True,
    )

    results = pandas.DataFrame.from_records(results)

    return results

def load_data_windowed():

    soundlevels_config = 'LAF'
    embeddings_config = 'yamnet-1'
    dataset = 'bcn'
    class_column = 'noise_class'

    project_root = get_project_root()

    # Load annotations
    classes = load_noise_classes()
    annotations = load_dataset_annotations().sort_index(level=(0, 1))
    annotations['noise_class'] = annotations.annotation.map(classes.noise.to_dict()).fillna('unknown')
    #print(annotations.head(3))

    # Create analysis windows
    window = pandas.Timedelta(seconds=0.96) # to match YAMNet size
    windows = annotation_to_windows(annotations, window=window, class_column=class_column)
    labeled = label_windows(windows)
    labeled = labeled.loc[dataset]
    #print(labeled.head())

    # Load preprocessed data
    soundlevel_path = os.path.join(project_root, f'data/processed/soundlevels/{soundlevels_config}.parquet')
    soundlevels = pandas.read_parquet(soundlevel_path).droplevel(0).loc[dataset].sort_index(level=(0, 1))
    
    embeddings_path = os.path.join(project_root, f'data/processed/embeddings/{embeddings_config}.parquet/')
    embeddings = pandas.read_parquet(embeddings_path).loc[dataset].sort_index(level=(0, 1))
    embeddings = embeddings.reset_index()
    embeddings['time'] = pandas.to_timedelta(embeddings['time'], unit='seconds')
    embeddings = embeddings.set_index(['clip', 'time'])

    # attach embeddings to windows
    merged = pandas.merge(labeled, embeddings.add_prefix('emb.'), right_index=True, left_index=True)
    assert len(merged) == len(labeled), (len(merged), len(labeled))

    return merged


def load_data_tracks():
   
    soundlevels_config = 'LAF'
    embeddings_config = 'yamnet-1'
    spectrogram_config = 'logmels-32bands-1024hop'
    dataset = 'bcn'
    class_column = 'noise_class'

    project_root = get_project_root()

    # Load annotations
    classes = load_noise_classes()
    annotations = load_dataset_annotations().loc[dataset].sort_index(level=(0, 1))
    annotations['noise_class'] = annotations.annotation.map(classes.noise.to_dict()).fillna('unknown')
    #print(annotations.head(3))

    # Load preprocessed data    
    embeddings_path = os.path.join(project_root, f'data/processed/embeddings/{embeddings_config}.parquet/')
    embeddings = pandas.read_parquet(embeddings_path).loc[dataset].sort_index(level=(0, 1))
    embeddings = embeddings.reset_index()
    embeddings['time'] = pandas.to_timedelta(embeddings['time'], unit='seconds')
    embeddings = embeddings.set_index(['clip', 'time']).drop(columns=['index'])


    # Load preprocessed data    
    spectrograms_path = os.path.join(project_root, f'data/processed/spectrograms/{spectrogram_config}.parquet')
    spectrograms = pandas.read_parquet(spectrograms_path).droplevel(0)
    print(spectrograms)
    spectrograms = spectrograms.loc[dataset].sort_index(level=(0, 1))
    #embeddings = embeddings.reset_index()
    #embeddings['time'] = pandas.to_timedelta(embeddings['time'], unit='seconds')
    #embeddings = embeddings.set_index(['clip', 'time']).drop(columns=['index'])


    return embeddings, spectrograms, annotations


def prepare_tracks(features, annotations,
        window_length = 100,
        downsample_ratio = 1,
        target_column='noise_class',
        overlap = 0.0,
        hop_duration = 0.48,
        ):

    # Create label tracks
    classes = sorted(annotations[target_column].unique())

    # Chop data into analysis windows
    feature_windows = []
    label_windows = []
    clip_windows = []
    window_indexes = []

    input_length = (downsample_ratio * window_length)

    for clip_idx, feat in features.groupby('clip'):
        feat = feat.droplevel(0)
        ann = annotations.loc[clip_idx]
        track = make_continious_labels(ann, length=int(len(feat)/downsample_ratio),
            time_resolution=hop_duration,
            class_column=target_column,
            classes=classes,
        )
        #assert len(track) == len(feat), (len(track), len(feat))
        #assert track.index.all() == feat.index.all()
        #print(feat.head())
        #print(track.head())
        class_activity = track.mean(axis=0)
        #print(class_activity)

        f = compute_windows(feat.values.T, frames=input_length, overlap=overlap)
        l = compute_windows(track.values.T, frames=window_length, overlap=overlap)
        assert len(f) == len(l)
        assert f.index.all() == l.index.all()

        #print('w', clip_idx, track.shape, feat.shape)

        window_indexes += [ track.index[i] for i in l.index ]
        feature_windows += list(f.values)
        label_windows += list(l.values)
        clip_windows += ([ clip_idx ] * len(f))

    windows = pandas.DataFrame({
        'features': feature_windows,
        'labels': label_windows,
        'clip': clip_windows,
        'window': window_indexes,
    }).set_index(['clip', 'window'])


    # Include class info as high level columns. For diagnostics
    class_activations = pandas.DataFrame(numpy.stack(windows.labels).sum(axis=2) / window_length, columns=classes, index=windows.index)
    windows = pandas.merge(windows, class_activations, left_index=True, right_index=True)

    return windows

def train_evaluate_tracks(windows, model,
        epochs = 500,
        batch_size = 8*64,
        ):

    X = numpy.stack([ w.T for w in windows['features']])
    Y = numpy.stack([ w.T for w in windows['labels']])

    # make sure to stop when model does not improve anymore / starts overfitting
    #early_stop = tensorflow.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

    from tqdm.keras import TqdmCallback
    progress_bar = TqdmCallback()
    tensorboard = keras.callbacks.TensorBoard(log_dir="logs")

    print('set', X.shape, Y.shape)
    print('Training start\n\n')

    # TODO: add support for Tensorboard
    hist = model.fit(x=X, y=Y,
        #validation_data=val,
        validation_split=0.25,
        epochs=epochs,
        batch_size=batch_size,
        verbose=False, # using progress bar callback instead
        callbacks=[
            progress_bar,
            #early_stop,
            tensorboard,
        ],

    )

    history = pandas.DataFrame(hist.history)
    fig = plot_history(history)
    fig.savefig('history.png')


def main():
    # FIXME: support data specified on input

    if False:

        windows = load_data_windowed().reset_index()

        label_counts = windows['label'].value_counts(dropna=False)
        print(label_counts)

        train_eval_windows(windows)

        return

    feature_size = 32
    downsample_ratio = 8
    hop_duration = 0.064*downsample_ratio
    window_duration = 10.0
    window_length = math.ceil(window_duration / hop_duration)
    input_length = downsample_ratio * window_length

    print('ww', window_length, input_length)

    # Load data
    embeddings, spectrograms, annotations = load_data_tracks()

    annotations['duration'] = annotations['end'] - annotations['start']

    # TEMP: limit to medium to long events
    annotations = annotations[annotations.duration > 1.0]

    # TEMP: limit to certain classes
    annotations = annotations[annotations.noise_class.isin(['road_traffic'])]

    class_durations = annotations.groupby('noise_class').duration.sum()
    print('class durations', class_durations)

    #assert embeddings.shape[1] == feature_size, embeddings.shape 

    n_classes = len(class_durations.index)
    model = build_model(input_shape=(input_length, feature_size),
        n_classes=n_classes,
        lr=0.01, dropout=0.00,
        name='sednet')
    model.summary()

    f = spectrograms
    windows = prepare_tracks(f, annotations,
        window_length=window_length,
        downsample_ratio=downsample_ratio,
        hop_duration=hop_duration,
    )
    print('windows', windows.shape)

    results = train_evaluate_tracks(windows, model)
    


if __name__ == '__main__':
    main()


