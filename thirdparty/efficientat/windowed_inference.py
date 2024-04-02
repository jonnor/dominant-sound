import torch
import librosa
import numpy as np
from torch import autocast
from contextlib import nullcontext

from thirdparty.efficientat.models.mn.model import get_model as get_mobilenet
from thirdparty.efficientat.models.ensemble import get_ensemble_model
from thirdparty.efficientat.models.preprocess import AugmentMelSTFT
from thirdparty.efficientat.helpers.utils import NAME_TO_WIDTH, labels

class EATagger:
    """
        EATagger: A class for tagging audio files with acoustic event tags.

        Parameters:

            model_name (str, optional): name of the pre-trained model to use.
            ensemble (str, optional): name of the ensemble of models to use.
            device (str, optional): device to run the model on, either 'cuda' or 'cpu'.
            sample_rate (int, optional): sample rate of the audio.
            window_size (int, optional): window size for audio analysis in samples.
            hop_size (int, optional): hop size for audio analysis in samples.
            n_mels (int, optional): number of mel bands to use for audio analysis.

        Methods:

            tag_audio_window(audio_path, window_size=20.0, hop_length=10.0): tags an audio file with an acoustic event.
                audio_path (str): path to the audio file
                window_size (float, optional): size of the window in seconds
                hop_length (float, optional): hop length in seconds
                
                Returns: list of dictionaries with the following keys:
                    'start': start time of the window in seconds
                    'end': end time of the window in seconds
                    'tags': list of tags for the window in dictionary format
                        'tag': name of the tag
                        'probability': confidence of the tag
    """
    def __init__(self,
        model_name=None,
        ensemble=None,
        device='cuda',
        sample_rate=32000,
        window_size=800,
        hop_size=320, 
        n_mels=128):

        self.device = torch.device('cuda') if device == 'cuda' and torch.cuda.is_available() else torch.device('cpu')
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.hop_size = hop_size
        self.n_mels = n_mels

        # load pre-trained model
        if ensemble is not None:
            self.model = get_ensemble_model(ensemble)
        elif model_name is not None:
            self.model = get_mobilenet(width_mult=NAME_TO_WIDTH(model_name), pretrained_name=model_name)
        else:
            raise ValueError('Please provide a model name or an ensemble of models')

        self.model.to(self.device)
        self.model.eval()

        # model to preprocess waveform into mel spectrograms
        self.mel = AugmentMelSTFT(n_mels=self.n_mels, sr=self.sample_rate, win_length=self.window_size, hopsize=self.hop_size)
        self.mel.to(self.device)
        self.mel.eval()

    def tag_audio_window(self, audio_path, window_size=1.0, hop_length=1.0):
        """
            Extracts embeddings from audio file and prediction scores for 527 AudioSet classes.
            Args:
                audio_path (str): path to the audio file
                window_size (float): size of the window in seconds
                hop_length (float): hop length in seconds
            Returns:
                Scores - A tensor of n class scores per inference window
                Features - A tensor of 960 coefficients per inference window

        """

        # load audio file
        (waveform, _) = librosa.core.load(audio_path, sr=self.sample_rate, mono=True)
        waveform = torch.from_numpy(waveform[None, :]).to(self.device)

        # analyze the audio file in windows, pad the last window if needed
        window_size = int(window_size * self.sample_rate)
        hop_length = int(hop_length * self.sample_rate)
        n_windows = int(np.ceil((waveform.shape[1] - window_size) / hop_length)) + 1
        waveform = torch.nn.functional.pad(waveform, (0, n_windows * hop_length + window_size - waveform.shape[1]))

        with torch.no_grad(), torch.autocast(
                device_type=self.device.type) if self.device.type == 'cuda' else nullcontext():

            scores = []
            feats = []
            for i in range(n_windows):
                start = i * hop_length
                end = start + window_size
                spec = self.mel(waveform[:, start:end])
                preds, features = self.model(spec.unsqueeze(0))
                preds = torch.sigmoid(preds.float()).squeeze().cpu().numpy()

                scores.append(preds)
                feats.append(features.numpy())

                print(f'\rProgress: {i + 1}/{n_windows}', end='')
            print()

        return scores, feats
        

if __name__ == '__main__':

    # load the model
    model = EATagger(model_name='mn10_as', device='cpu')

    # extract scores and features
    scores, feats = model.tag_audio_window('resources/metro_station-paris.wav', window_size=1.0, hop_length=1.0)

    print(scores[0])
    print(feats[0])
