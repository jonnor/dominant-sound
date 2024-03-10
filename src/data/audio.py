
import os.path

def get_audio_path(dataset : str, file_id: str = '09', audio_root=None):

    dataset_dir = {
        'tut': 'tut_ds/TUT-sound-events-2017-development/audio/',
        'maestro': 'maestro_ds/development_audio/',
    }

    dir = os.path.join(audio_root, dataset_dir[dataset])

    if dataset == 'maestro':
        scene = '_'.join(file_id.split('_')[:-1])
        filename = os.path.join(dir, scene, f'{file_id}.wav')
    else:
        scene = 'street'
        filename = os.path.join(dir, scene, f'{file_id}.wav')

    assert os.path.exists(filename), filename
    return filename

