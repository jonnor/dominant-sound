# Efficient Pre-Trained CNNs for Audio Pattern Recognition

Stripped-down fork of the [Efficient AT](https://github.com/fschmid56/EfficientAT) repository - purely intended for loading pre-trained models to perform inference on audio files and return their embeddings and class predictions.

Efficient AT pre-trained models and the code described in the papers:
* [Efficient Large-Scale Audio Tagging Via Transformer-To-CNN Knowledge Distillation](https://arxiv.org/pdf/2211.04772.pdf). The paper has been presented in 
[ICASSP 2023](https://2023.ieeeicassp.org/) and is published in IEEE 
([published version](https://ieeexplore.ieee.org/abstract/document/10096110?casa_token=_FKutWF2kxIAAAAA:vtUj5_FKRHVxfWIs0nU4-GqW3jDkj6twAPaCxQrdV81AeiDcINsQU_zCK-iZZbJAHJXTRZZCkm3z)). 
* [Dynamic Convolutional Neural Networks as Efficient Pre-trained Audio
Models](https://arxiv.org/pdf/2310.15648.pdf). Submitted to IEEE/ACM TASLP. **Pre-trained Models included, experiments on downstream tasks will be updated!**


## Environment

The codebase is developed with *Python 3.10.8*. After creating an environment install the requirements as
follows:

```
pip install -r requirements.txt
```

Also make sure you have FFmpeg <v4.4 installed.

## Pre-Trained Models



**Pre-trained models are available in the Github Releases and are automatically downloaded from there.** 
Loading the pre-trained models is as easy as inserting the model name into the EATagger class as demonstarated below:


The Table shows a selection of models contained in this repository. The naming convention for our models is 
**<model\>\<width_mult\>\_\<dataset\>**. In this sense, *mn10_as* defines a MobileNetV3 with parameter *width_mult=1.0*, pre-trained on 
AudioSet. *dymn* is the prefix for a dynamic MobileNet.

All models available are pre-trained on ImageNet [9] by default (otherwise denoted as 'no_im_pre'), followed by training on AudioSet [4]. Some results appear slightly better than those reported in the
papers. We provide the best models in this repository while the paper is showing averages over multiple runs.

| Model Name       | Config                                             | Params (Millions) | MACs (Billions) | Performance (mAP) |
|------------------|----------------------------------------------------|-------------------|-----------------|-------------------|
| dymn04_as        | width_mult=0.4                                     | 1.97              | 0.12            | 45.0              |
| dymn10_as        | width_mult=1.0                                     | 10.57             | 0.58            | 47.7              |
| dymn20_as        | width_mult=2.0                                     | 40.02             | 2.2             | 49.1              |
| mn04_as          | width_mult=0.4                                     | 0.983             | 0.11            | 43.2              |
| mn05_as          | width_mult=0.5                                     | 1.43              | 0.16            | 44.3              |
| mn10_as          | width_mult=1.0                                     | 4.88              | 0.54            | 47.1              |
| mn20_as          | width_mult=2.0                                     | 17.91             | 2.06            | 47.8              |
| mn30_as          | width_mult=3.0                                     | 39.09             | 4.55            | 48.2              |
| mn40_as          | width_mult=4.0                                     | 68.43             | 8.03            | 48.4              |
| mn40_as_ext      | width_mult=4.0,<br/>extended training (300 epochs) | 68.43             | 8.03            | 48.7              |
| mn40_as_no_im_pre      | width_mult=4.0, no ImageNet pre-training           | 68.43             | 8.03            | 48.3              |
| mn10_as_hop_15   | width_mult=1.0                                     | 4.88              | 0.36            | 46.3              |
| mn10_as_hop_20   | width_mult=1.0                                     | 4.88              | 0.27            | 45.6              |
| mn10_as_hop_25   | width_mult=1.0                                     | 4.88              | 0.22            | 44.7              |
| mn10_as_mels_40  | width_mult=1.0                                     | 4.88              | 0.21            | 45.3              |
| mn10_as_mels_64  | width_mult=1.0                                     | 4.88              | 0.27            | 46.1              |
| mn10_as_mels_256 | width_mult=1.0                                     | 4.88              | 1.08            | 47.4              |
| MN Ensemble         | width_mult=4.0, 9 Models                           | 615.87            | 72.27           | 49.8              |

MN Ensemble denotes an ensemble of 9 different mn40 models (3x mn40_as,
3x mn40_as_ext, 3x mn40_as_no_im_pre).

Note that computational complexity strongly depends on the resolution of the spectrograms. Our default is 128 mel bands and a hop size of 10 ms.

## Inference

You can use the pre-trained models for inference on an audio file by creating an instance of the "EATagger" class from the  
[windowed_inference.py](windowed_inference.py) script and calling the "tag_audio_window" function.

For example, use **mn10_as** to detect acoustic events at a metro station in paris:

```
model = EATagger(model_name='mn10_as', device='cpu')
scores, feats = model.tag_audio_window('resources/metro_station-paris.wav', window_size=1.0, hop_length=1.0)
```

This will output two vectors of 527 "scores" and 960 "embeddings" per inference window
