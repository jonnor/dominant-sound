
"""
Modified from PANNs code in order to get access to frame-wise embeddings

Has the following modifications:

Cnn14_DecisionLevelMax provides an additional output, framewise_embedding
SoundEventDetection provides an additional method, embed()
Both classes take a new parameter, interpolate_ratio
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import librosa
import panns_inference
from panns_inference import AudioTagging, SoundEventDetection, labels

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.checkpoint as cp
from torch.nn.parameter import Parameter

from torchlibrosa.stft import Spectrogram, LogmelFilterBank
from torchlibrosa.augmentation import SpecAugmentation
from panns_inference.pytorch_utils import do_mixup, pad_framewise_output, Interpolator

from panns_inference.models import ConvBlock, init_layer, init_bn

from pathlib import Path

from panns_inference.pytorch_utils import move_data_to_device
from panns_inference.config import labels, classes_num

class Cnn14_DecisionLevelMax(nn.Module):
    def __init__(self, sample_rate, window_size, hop_size, mel_bins, fmin, 
        fmax, classes_num, interpolate_mode='nearest', interpolate_ratio=32):
        
        super(Cnn14_DecisionLevelMax, self).__init__()

        window = 'hann'
        center = True
        pad_mode = 'reflect'
        ref = 1.0
        amin = 1e-10
        top_db = None
        self.interpolate_ratio = interpolate_ratio     # Downsampled ratio

        # Spectrogram extractor
        self.spectrogram_extractor = Spectrogram(n_fft=window_size, hop_length=hop_size, 
            win_length=window_size, window=window, center=center, pad_mode=pad_mode, 
            freeze_parameters=True)

        # Logmel feature extractor
        self.logmel_extractor = LogmelFilterBank(sr=sample_rate, n_fft=window_size, 
            n_mels=mel_bins, fmin=fmin, fmax=fmax, ref=ref, amin=amin, top_db=top_db, 
            freeze_parameters=True)

        # Spec augmenter
        self.spec_augmenter = SpecAugmentation(time_drop_width=64, time_stripes_num=2, 
            freq_drop_width=8, freq_stripes_num=2)

        self.bn0 = nn.BatchNorm2d(64)

        self.conv_block1 = ConvBlock(in_channels=1, out_channels=64)
        self.conv_block2 = ConvBlock(in_channels=64, out_channels=128)
        self.conv_block3 = ConvBlock(in_channels=128, out_channels=256)
        self.conv_block4 = ConvBlock(in_channels=256, out_channels=512)
        self.conv_block5 = ConvBlock(in_channels=512, out_channels=1024)
        self.conv_block6 = ConvBlock(in_channels=1024, out_channels=2048)

        self.fc1 = nn.Linear(2048, 2048, bias=True)
        self.fc_audioset = nn.Linear(2048, classes_num, bias=True)

        self.interpolator = Interpolator(
            ratio=self.interpolate_ratio, 
            interpolate_mode=interpolate_mode
        )
        
        self.init_weight()

    def init_weight(self):
        init_bn(self.bn0)
        init_layer(self.fc1)
        init_layer(self.fc_audioset)
 
    def forward(self, input, mixup_lambda=None):
        """
        Input: (batch_size, data_length)"""

        x = self.spectrogram_extractor(input)   # (batch_size, 1, time_steps, freq_bins)
        x = self.logmel_extractor(x)    # (batch_size, 1, time_steps, mel_bins)

        frames_num = x.shape[2]
        
        x = x.transpose(1, 3)
        x = self.bn0(x)
        x = x.transpose(1, 3)
        
        if self.training:
            x = self.spec_augmenter(x)

        # Mixup on spectrogram
        if self.training and mixup_lambda is not None:
            x = do_mixup(x, mixup_lambda)

        x = self.conv_block1(x, pool_size=(2, 2), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv_block2(x, pool_size=(2, 2), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv_block3(x, pool_size=(2, 2), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv_block4(x, pool_size=(2, 2), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv_block5(x, pool_size=(2, 2), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv_block6(x, pool_size=(1, 1), pool_type='avg')
        x = F.dropout(x, p=0.2, training=self.training)
        x = torch.mean(x, dim=3)
        
        x1 = F.max_pool1d(x, kernel_size=3, stride=1, padding=1)
        x2 = F.avg_pool1d(x, kernel_size=3, stride=1, padding=1)
        x = x1 + x2
        x = F.dropout(x, p=0.5, training=self.training)
        x = x.transpose(1, 2)
        x = F.relu_(self.fc1(x))
        x = F.dropout(x, p=0.5, training=self.training)
        segmentwise_output = torch.sigmoid(self.fc_audioset(x))
        (clipwise_output, _) = torch.max(segmentwise_output, dim=1)

        # Get framewise output
        framewise_output = self.interpolator(segmentwise_output)
        framewise_output = pad_framewise_output(framewise_output, frames_num)

        # MODIFIED. The framewise_embedding 
        output_dict = {
            'framewise_embedding': x,
            'framewise_output': framewise_output,
            'clipwise_output': clipwise_output,
        }

        return output_dict

class SoundEventDetection(object):
    def __init__(self, model=None, checkpoint_path=None, device='cuda', interpolate_mode='nearest', interpolate_ratio=32):
        """Sound event detection inference wrapper.

        Args:
            model: None | nn.Module
            checkpoint_path: str
            device: str, 'cpu' | 'cuda'
            interpolate_mode, 'nearest' |'linear'
        """
        if not checkpoint_path:
            checkpoint_path='{}/panns_data/Cnn14_DecisionLevelMax.pth'.format(str(Path.home()))
        print('Checkpoint path: {}'.format(checkpoint_path))

        if not os.path.exists(checkpoint_path) or os.path.getsize(checkpoint_path) < 3e8:
            create_folder(os.path.dirname(checkpoint_path))
            os.system('wget -O "{}" https://zenodo.org/record/3987831/files/Cnn14_DecisionLevelMax_mAP%3D0.385.pth?download=1'.format(checkpoint_path))

        if device == 'cuda' and torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        
        self.labels = labels
        self.classes_num = classes_num

        # Model
        if model is None:
            self.model = Cnn14_DecisionLevelMax(sample_rate=32000, window_size=1024, 
                hop_size=320, mel_bins=64, fmin=50, fmax=14000, 
                classes_num=self.classes_num, interpolate_mode=interpolate_mode, interpolate_ratio)
        else:
            self.model = model
        
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model'])

        # Parallel
        if 'cuda' in str(self.device):
            self.model.to(self.device)
            print('GPU number: {}'.format(torch.cuda.device_count()))
            self.model = torch.nn.DataParallel(self.model)
        else:
            print('Using CPU.')

    def inference(self, audio, output='framewise_output'):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(
                input=audio, 
                mixup_lambda=None
            )

        framewise_output = output_dict[output].data.cpu().numpy()

        return framewise_output

    # MODIFIED: this method is new
    def embed(self, audio):
        return self.inference(audio, output='framewise_embedding')

