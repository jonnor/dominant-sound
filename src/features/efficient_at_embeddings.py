import os
import pandas
import numpy
from src.utils.fileutils import get_project_root, ensure_dir
from src.data.audio import get_audio_path
from src.data.annotations import load_dataset_annotations

from thirdparty.efficientat.windowed_inference import EATagger


def process_audio(audio_path: str,
                  win_size: float,
                  hop_length: float,
                  model,
                  audio_time: float = 0.0):

    # EfficientAT needs 32kHz sample rate
    sr = 32000

    # generate embeddings

    # EfficientAT code
    scores, embeddings = model.tag_audio_window(audio_path=audio_path, window_size=win_size, hop_length=hop_length)

    scores = numpy.asarray(scores)
    embeddings = numpy.asarray(embeddings).squeeze(1)

    # Convert to nice dataframes
    sc = pandas.DataFrame(scores, columns=[f'c{i}' for i in range(scores.shape[1])])
    sc['time'] = audio_time + numpy.arange(0, len(sc)) * hop_length
    del scores # free memory

    emb = pandas.DataFrame(embeddings, columns=[f'e{i}' for i in range(embeddings.shape[1])])
    emb['time'] = audio_time + numpy.arange(0, len(emb)) * hop_length
    print(emb['time'].head(10))
    del embeddings # free memory

    return sc, emb


def process_datasets(eat_model_id: str = 'mn10_as_hop_5'):
    """
    Compute and store EfficientAT scores and embeddings for the datasets
    """

    eat_model = EATagger(model_name=eat_model_id, device='cpu')

    project_root = get_project_root()
    audio_root = os.path.join(project_root, 'data/raw/')
    scores_dir = os.path.join(project_root, 'data/processed/scores_EAT/')
    ensure_dir(scores_dir)
    embeddings_dir = os.path.join(project_root, 'data/processed/embeddings_EAT/')
    ensure_dir(embeddings_dir)

    # load the annotations file for clip info
    annotations = load_dataset_annotations()

    files = annotations.reset_index().set_index(['dataset', 'clip']).index.unique()
    files = files.to_frame()

    for row in files.index:
        dataset = files.loc[row, 'dataset']
        clip = files.loc[row, 'clip']
        path = get_audio_path(dataset=dataset, file_id=clip, audio_root=audio_root)

        sc, emb = process_audio(audio_path=path, win_size=1.0, hop_length=1.0, model=eat_model)

        sc_path = os.path.join(scores_dir, f'{dataset}_{clip}.parquet')
        sc.to_parquet(sc_path)

        emb_path = os.path.join(embeddings_dir, f'{dataset}_{clip}.parquet')
        emb.to_parquet(emb_path)


if __name__ == "__main__":
    # for testing purposes
    model = EATagger(model_name='mn10_as_hop_5', device='cpu')
    scores, feats = process_audio(audio_path='../../thirdparty/efficientat/resources/metro_station-paris.wav',
                                  win_size=1.0, hop_length=1.0, model=model)
    print(scores)
    print(feats)

    # process_datasets()
