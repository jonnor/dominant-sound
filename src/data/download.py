import os
import urllib.request
import zipfile
from src.utils.fileutils import get_project_root

root_path = get_project_root()
download_path = os.path.join(root_path, 'data/raw')


def maestro():

    base_url = 'https://zenodo.org/records/7244360/files'

    # Target URLs for the dataset files on Zenodo
    audio_zip = os.path.join(base_url, 'development_audio.zip')
    annotation_zip = os.path.join(base_url, 'development_annotation.zip')
    license_txt = os.path.join(base_url, 'LICENSE.txt')
    readme_md = os.path.join(base_url, 'README.md')

    # Specify and create the target directory for the dataset
    target_path = os.path.join(download_path, 'maestro_ds')

    if not os.path.exists(target_path):
        os.makedirs(target_path)

        # download the zip files
        urllib.request.urlretrieve(audio_zip, os.path.join(target_path, 'development_audio.zip'))
        urllib.request.urlretrieve(annotation_zip, os.path.join(target_path, 'development_annotation.zip'))

        # download the license and readme
        urllib.request.urlretrieve(license_txt, os.path.join(target_path, 'LICENSE.txt'))
        urllib.request.urlretrieve(readme_md, os.path.join(target_path, 'README.md'))

        # Extract the zip files and tidy up
        zips = [i for i in os.listdir(target_path) if i.endswith('.zip')]

        for f in zips:
            with zipfile.ZipFile(os.path.join(target_path, f), 'r') as zip_ref:
                zip_ref.extractall(target_path)

            os.remove(os.path.join(target_path, f))

    else:
        print(f'Dataset downloaded - see "data/raw/maestro_ds" directory')


def tut():

    base_url = 'https://zenodo.org/records/814831/files'

    # Target URLs for the dataset files on Zenodo
    audio_1_zip = os.path.join(base_url, 'TUT-sound-events-2017-development.audio.1.zip')
    audio_2_zip = os.path.join(base_url, 'TUT-sound-events-2017-development.audio.2.zip')
    dev_meta = os.path.join(base_url, 'TUT-sound-events-2017-development.meta.zip')
    dev_doc = os.path.join(base_url, 'TUT-sound-events-2017-development.doc.zip')

    # Specify and create the target directory for the dataset
    target_path = os.path.join(download_path, 'tut_ds')

    if not os.path.exists(target_path):
        os.makedirs(target_path)

        # download the zip files
        urllib.request.urlretrieve(audio_1_zip, os.path.join(target_path, 'development_audio_1.zip'))
        urllib.request.urlretrieve(audio_2_zip, os.path.join(target_path, 'development_audio_2.zip'))
        urllib.request.urlretrieve(dev_meta, os.path.join(target_path, 'development_meta.zip'))
        urllib.request.urlretrieve(dev_doc, os.path.join(target_path, 'development_doc.zip'))

        zips = [i for i in os.listdir(target_path) if i.endswith('.zip')]

        for f in zips:
            with zipfile.ZipFile(os.path.join(target_path, f), 'r') as zip_ref:
                zip_ref.extractall(target_path)

            os.remove(os.path.join(target_path, f))

    else:
        print(f'Dataset downloaded - see "data/raw/tut_ds" directory')


def fetch_all():
    maestro()
    tut()
    print('Datasets downloaded: see "data/raw/..."')
