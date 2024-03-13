
## Datasets

#### DCASE2017 - Sound event detection in real life audio
https://dcase.community/challenge2017/task-sound-event-detection-in-real-life-audio
Captured on city streets in Finland. Recordings are 3-5 minutes long.
Labeled with events.
Classes: brakes squeaking, car, children, large vehicle, people speaking, people walking
2 GB total.

Could be used to study how often sounds co-occur?

#### DCASE2023 - Sound Event Detection with Soft Labels
https://dcase.community/challenge2023/task-sound-event-detection-with-soft-labels#baseline-system
Aka MAESTRO Real dataset.

Real outdoors recordings. Approx 3 minutes each.
2.6 GB total.

Birds singing, Car, People talking, Footsteps, Children voices, Wind blowing, Brakes squeaking,
Large vehicle, Cutlery and dishes, Metro approaching, Metro leaving.
Contains labels for both road noise, rail noise, community noise.
Also contains labels for geophony and biophony.

Could be used to study how often sounds co-occur?

#### SONYC-UST v2
https://zenodo.org/record/3966543
10 second clips. Tagged with the classes.
Has good class taxonomy - designed for (urban) noise monitoring.
8 high-level classes. 23 fine-grained.

Could be possible to re-annotate with the dominant class?
Could be used to study how often sounds co-occur?


#### SINGA:PURA
A Strongly-Labelled Polyphonic Dataset of Urban Sounds with Spatiotemporal Context
https://arxiv.org/abs/2111.02006

Downloadable from
https://researchdata.ntu.edu.sg/dataset.xhtml?persistentId=doi:10.21979/N9/Y8UQ6F

Uses the SONYC-UST ontology as a basis.
Adds other classed in addition.
13 coarse labels in total.

6547 recordings of 10 seconds were annotated, totaling to 18.2 hours of audio data.
Shows number of overlapping events.

#### InspectNoise
RaveGuard: A Noise Monitoring Platform Using Low-End Microphones and Machine Learning 
2020

https://www.mdpi.com/1424-8220/20/19/5583

https://github.com/LorenzoMonti/inspectNoise/tree/master/dataset
No audio published? Just soundlevels?

#### NoisenseDB

NoisenseDB: An Urban Sound Event Database to Develop Neural Classification Systems for Noise-Monitoring Applications

https://www.mdpi.com/2076-3417/13/16/9358

NoisenseDB is available upon request to itxasne@noismart.com.
No license mentioned.

Extracted a set of variable-length audio clips corresponding to the sound events that registered
a peak level equal or greater than 71 dB(A)
and kept above 60 dB(A) during at least 3 consecutive seconds.

Total of 432 sound clips with labels.
Two level taxonomy. Traffic, human, nature, mechanical on top.
Pre split in 5 folds.
Also have 260 for unsupervised learning, no labels.
Between 6 and 120 seconds.


#### DCASE 2019 Task 4 
https://dcase.community/challenge2022/task-sound-event-detection-in-domestic-environments

Aka Domestic Environment Sound Event Detection (DESED) dataset

10 sec audio clips recorded in domestic environment or synthesized to simulate a domestic environment.

Seems less relevant.

### USM-SED
USM-SED - A Dataset for Polyphonic Sound Event Detection in Urban Sound Monitoring Scenarios
https://arxiv.org/abs/2105.02592
FSD50k dataset, 20,000 polyphonic soundscapes are synthesized
https://github.com/jakobabesser/USM
AES 2022 paper
https://github.com/jakobabesser/USM/blob/main/paper/Abesser_2022_UrbanSoundsPreprint_AES.pdf
6 sound categories, covering 26 classes. 

Syntetic, cannot assume to be entierly realistic.
? should have information on the soundlevel contribution of each input

USM-SED dataset includes both the audio mix (sound scene),
and the corresponding single tracks (stems) and hence provides a suitable test-bed for source separation algorithms.

Downloadable from
https://zenodo.org/records/6413788
10 files a 4 GB.

### URBAN-SED

http://urbansed.weebly.com/

Syntetic, cannot assume to be realistic.

### Isolated urban sound database
https://zenodo.org/records/1213793

Has background and event sounds. Designed to be mixed together.

Event. Includes includes 231 brief sound samples considered as salient,
with a 1 to 20 seconds duration and classified among 21 sound classes.
Ringing bell, whistling bird, car horn, passing car, hammer, barking dog, siren, footstep, metallic noise, voice...
Background. Includes 162 long duration sounds (~1mn30), whose acoustic properties do not vary in time.
This category includes among others, whistling bird, crowd noise, rain, children playing in schoolyard, constant traffic noise...

### MAVD-traffic dataset
https://zenodo.org/records/4741232
Montevideo Audio and Video Dataset.
This is a dataset for sound event detection in urban environments.
The sound event annotations follow an ontology for traffic sounds that is the combination of a set of two taxonomies: vehicle types (e.g. car, bus) and vehicle components (e.g.engine, brakes), and a set of actions related to them (e.g. idling, accelerating).

Presented in "MAVD: a dataset for sound event detection in urban environments." DCASE 2019 Workshop.

### Test dataset for separation of speech, traffic sounds, wind noise, and general sounds

https://zenodo.org/records/4279220
It contains various sounds from the Audio Set [1] and spoken utterances from VCTK [2] and DNS [3] datasets.
Used in paper,
Deep Complex U-Net Ensemble for Outdoor Urban Sound Source Separation.


### BCN Dataset: an Annotated Night Urban Sounds dataset
https://zenodo.org/records/3956503

! highly relevant work

Contains 363 minutes of real-world audio recordings made at the city center of Barcelona.
Audacity labels.
Can be easily downloaded.

BCNDataset: Description and Analysis of an Annotated Night Urban Leisure Sound Dataset 
https://www.mdpi.com/2071-1050/12/19/8140
by Ester Vidaña-Vila, Leticia Duboc, Rosa Ma Alsina-Pagès, Francesc Polls
Sustainability 2020


#### Multilabel Acoustic Event Classification Using Real-World Urban Data and Physical Redundancy of Sensors 
https://www.mdpi.com/1424-8220/21/22/7470

Propose a two-stage classifier able to identify, in real time, a set of up to 21 urban acoustic events that may occur simultaneously (i.e., multilabel), taking advantage of physical redundancy in acoustic sensors from a wireless acoustic sensors network. The first stage of the proposed system consists of a multilabel deep neural network that makes a classification for each 4-s window. The second stage intelligently aggregates the classification results from the first stage of four neighboring nodes to determine the final classification result.

MobileNet v2 as base for first stage.
RandomForest etc as second stage.
Real time factor of 50% on RPI Model 2B

A new real-world 5 h length dataset (containing concurrent events) recorded simultaneously at four spots from a street intersection.
!? dataset not available.
Also uses BCNDataset for eval.

Analysis and Acoustic Event Classification of Environmental Data Collected in a Citizen Science Project 
https://www.mdpi.com/1660-4601/20/4/3683
Sons al Balcó project.
No data available either...

#### Other

https://dcase.community/challenge2023/task-sound-event-detection-with-weak-labels-and-synthetic-soundscapes 

Synthetic, cannot assume to be realistic.
