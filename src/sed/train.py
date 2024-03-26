
from src.utils.fileutils import get_project_root
from src.data.annotations import load_noise_classes, load_dataset_annotations, count_events_in_period

import os

import pandas
import tensorflow.keras

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


def build_model(input_shape, dropout=0.5, lr=0.01, class_weights=None, name='sedgru'):

    from .models import build_sedgru, build_sednet
    
    # Model
    if name == 'sednet':
        model = build_sednet(input_shape, n_classes=1,
                         filters=10,
                         cnn_pooling=[2, 2, 2],
                         rnn_units=[5, 5],
                         dense_units=[16],
                         dropout=dropout,
                        )
    elif name == 'sedgru':
        model = build_sedgru(input_shape, n_classes=1,
                             reduction_units=(8,),
                             rnn_units=[5, 5],
                             dense_units=[16],
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
    history = pandas.DataFrame(hist.history)
    history.index.name = 'epoch'
    history.plot(ax=axs[0], y=['loss', 'val_loss'])
    history.plot(ax=axs[1], y=['pr_auc', 'val_pr_auc'])
    axs[1].set_ylim(0, 1.0)
    axs[1].axhline(0.40, ls='--', color='black', alpha=0.5)
    
    axs[0].axhline(0.10, ls='--', color='black', alpha=0.5)
    axs[0].set_ylim(0, 1.0)


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



def main():
    # FIXME: support data specified on input

    soundlevels_config = 'LAF'
    embeddings_config = 'yamnet-1'

    project_root = get_project_root()

    # Load annotations
    classes = load_noise_classes()
    annotations = load_dataset_annotations().sort_index(level=(0, 1))
    annotations['noise_class'] = annotations.annotation.map(classes.noise.to_dict()).fillna('unknown')
    print(annotations.head(3))

    files = annotations.reset_index().set_index(['dataset', 'clip']).index.unique()
    files = files.to_frame()
    print(files.head())

    window = pandas.Timedelta(seconds=0.96) # to match YAMNet size
    windows = annotation_to_windows(annotations, window=window, class_column='noise_class')
    print(windows)

    # Load preprocessed data
    soundlevel_path = os.path.join(project_root, f'data/processed/soundlevels/{soundlevels_config}.parquet')
    soundlevels = pandas.read_parquet(soundlevel_path).droplevel(0).sort_index(level=(0, 1))
    
    embeddings_path = os.path.join(project_root, f'data/processed/embeddings/{embeddings_config}.parquet/')
    embeddings = pandas.read_parquet(embeddings_path).sort_index(level=(0, 1, 2))

    print(embeddings.shape)
    print(embeddings.head(10))

    return

    model = build_model(input_shape=(window_length, 32))

    epochs = 400
    batch_size = 8*64

    # Compute the spectral background across entire clip
    # Used for spectral subtraction, a type of preprocessing/normalization technique that is often useful
    Xm = numpy.expand_dims(numpy.mean(numpy.concatenate([s.T for s in dataset.spectrogram]), axis=0), -1)

    class_weights = compute_class_weights(train[1])
    #class_weights = None # disable class weights
    print('Class weights', class_weights)

    # make sure to stop when model does not improve anymore / starts overfitting
    early_stop = tensorflow.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

    from tqdm.keras import TqdmCallback
    progress_bar = TqdmCallback()

    # TODO: add support for Tensorboard
    hist = model.fit(x=train[0], y=train[1],
        validation_data=val,
        epochs=epochs,
        batch_size=batch_size,
        verbose=False, # using progress bar callback instead
        callbacks=[
            progress_bar,
            #lr_callback,
            #early_stop,
        ],

    )

    plot_history(hist)    

if __name__ == '__main__':
    main()


