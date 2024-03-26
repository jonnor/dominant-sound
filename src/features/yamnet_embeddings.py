
import os
import sys
import time

import tensorflow
import tensorflow_hub
import pandas
import numpy
import librosa
import structlog

log = structlog.get_logger()

def audio_chunks_from_file(path, sr, chunk=600.0, start=0.0):
    """
    Generator that yields audio chunks from file
    """

    audio_load_duration = 0.0
    embed_duration = 0.0

    # do the processing in chunks, to keep memory usage down
    clip_duration = librosa.get_duration(path=path)
    position = start
    remaining = clip_duration
    while remaining > 0.0:
        audio_load_start = time.time()
        audio, sr = librosa.load(path, sr=sr, offset=position, duration=min(chunk, remaining))
        audio_load_duration += (time.time() - audio_load_start)
        stats = dict(load_duration=audio_load_duration, audio_seconds=float(position))

        chunk_duration = len(audio)/sr
        position += chunk_duration
        remaining = clip_duration - position
        yield audio, stats

def process_audio(yamnet_model, audio, audio_time, sr=16000):

    # generate embeddings
    embed_start = time.time()
    scores_tensor, embedding_tensor, spectrogram = yamnet_model(tensorflow.convert_to_tensor(audio))
    embeddings = embedding_tensor.numpy()
    scores = scores_tensor.numpy()
    embed_end = time.time()

    # sanity checks
    assert len(scores) == len(embeddings)
    hop_duration = 0.480
    frame_duration = 0.010
    effective_hop = (len(audio)/sr) / embeddings.shape[0]
    effective_frame = (len(audio)/sr) / spectrogram.shape[0]
    assert abs(effective_hop-hop_duration) < 0.01
    assert abs(effective_frame-frame_duration) < 0.01

    # Convert to nice dataframes
    # FIXME: use proper class identifiers
    sc = pandas.DataFrame(scores, columns=[f'c{i}' for i in range(scores.shape[1])])
    sc['time'] = audio_time + numpy.arange(0, len(sc)) * hop_duration
    del scores # free memory

    emb = pandas.DataFrame(embeddings, columns=[f'e{i}' for i in range(embeddings.shape[1])])
    emb['time'] = audio_time + numpy.arange(0, len(emb)) * hop_duration
    print(emb['time'].head(10))
    del embeddings # free memory

    spec = pandas.DataFrame(spectrogram, columns=[f's{i}' for i in range(spectrogram.shape[1]) ])
    spec['time'] = audio_time + numpy.arange(0, len(spec)) * frame_duration
    del spectrogram # free memory

    return sc, emb, spec


def process_audio_file(path,
        save_embedding=None,
        save_spectrogram=None,
        chunk=600.0,
        start = 0.0,
        ):

    # load model
    model_load_start = time.time()
    yamnet_model = tensorflow_hub.load('https://tfhub.dev/google/yamnet/1')
    model_load_end = time.time()

    # load audio
    audio_load_start = time.time()
    sr = 16000 # yamnet works with 16khz only

    audio_load_duration = 0.0
    embed_duration = 0.0

    # do the processing in chunks, to keep memory usage down

    audio_generator = audio_chunks_from_file(path, sr=sr, chunk=chunk, start=start)
    for audio, audio_stats in audio_generator:

        embed_start = time.time()
        sc, emb, spec = process_audio(yamnet_model, audio, audio_time=audio_stats['audio_seconds'])
        embed_duration += (time.time() - embed_start)

        log.info("embed-audio-chunk",
            #offset=position,
            returned=len(audio)/sr,
        )

        yield sc, emb, spec

    # diagnostics
    model_load_duration = model_load_end-model_load_start
    audio_load_duration = audio_stats['load_duration']

    stats = dict(
        audio_length=audio_stats['audio_seconds'],
        model_load=round(model_load_duration, 3),
        audio_load=round(audio_load_duration, 3),
        #save=round(save_duration, 3),
        embedding=round(embed_duration, 3),
    )

    log.info('embed-audio-file',
        path=path,
        **stats,
    )

    return stats


