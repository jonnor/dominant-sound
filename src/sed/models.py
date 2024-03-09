
def build_sednet(input_shape,
    filters=128,
    cnn_pooling=(5, 2, 2),
    rnn_units=(32, 32),
    dense_units=(32,),
    n_classes=1,
    dropout=0.5
    ):
    """
    SEDnet type model. A CRNN

    Based https://github.com/sharathadavanne/sed-crnn/blob/master/sed.py
    """
    
    from tensorflow.keras import Model
    from tensorflow.keras.layers import Input, Bidirectional, Conv2D, BatchNormalization, Activation, \
            Dense, MaxPooling2D, Dropout, Permute, Reshape, GRU, TimeDistributed
    
    spec_start = Input(shape=(input_shape[-2], input_shape[-1]))

    # add 
    cnn_shape = (input_shape[-2], input_shape[-1], 1)
    spec_x = Reshape(cnn_shape)(spec_start)

    # Convolutional layers
    for i, pool in enumerate(cnn_pooling):
        spec_x = Conv2D(filters=filters, kernel_size=(3, 3), padding='same')(spec_x)
        spec_x = BatchNormalization(axis=1)(spec_x)
        spec_x = Activation('relu')(spec_x)
        spec_x = MaxPooling2D(pool_size=(1, pool))(spec_x)
        spec_x = Dropout(dropout)(spec_x)
    spec_x = Permute((2, 1, 3))(spec_x)
    spec_x = Reshape((input_shape[-2], -1))(spec_x)

    # Recurrent layers
    for units in rnn_units:
        spec_x = Bidirectional(
            GRU(units, activation='tanh', dropout=dropout, recurrent_dropout=dropout, return_sequences=True),
            merge_mode='mul')(spec_x)

    # Classifier
    for units in dense_units:
        spec_x = TimeDistributed(Dense(units))(spec_x)
        spec_x = Dropout(dropout)(spec_x)

    spec_x = TimeDistributed(Dense(n_classes))(spec_x)
    out = Activation('sigmoid', name='strong_out')(spec_x)
    
    model = Model(inputs=spec_start, outputs=out)
    
    return model


def build_sedgru(input_shape,
    filters=128,
    reduction_units=(16,),
    rnn_units=(32, 32),
    dense_units=(32,),
    n_classes=1,
    dropout=0.5,
    ):
    """
    Per-timestep feature transformation followed by RNN
    """
    
    from tensorflow.keras import Model
    from tensorflow.keras.layers import Input, Bidirectional, Conv2D, BatchNormalization, Activation, \
            Dense, MaxPooling2D, Dropout, Permute, Reshape, GRU, TimeDistributed
    
    spec_start = Input(shape=(input_shape[-2], input_shape[-1]))
    spec_x = spec_start

    # Dimensionality reduction with dense layers
    for units in reduction_units:
        spec_x = TimeDistributed(Dense(units, activation='relu'))(spec_x)
    
    for units in rnn_units:
        spec_x = Bidirectional(
            GRU(units, activation='tanh', dropout=dropout, recurrent_dropout=dropout, return_sequences=True),
            merge_mode='mul')(spec_x)

    for units in dense_units:
        spec_x = TimeDistributed(Dense(units))(spec_x)
        spec_x = Dropout(dropout)(spec_x)

    spec_x = TimeDistributed(Dense(n_classes))(spec_x)
    out = Activation('sigmoid', name='strong_out')(spec_x)
    
    model = Model(inputs=spec_start, outputs=out)
    
    return model

