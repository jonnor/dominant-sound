
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

FSD50k dataset, 20,000 polyphonic soundscapes are synthesized

Syntetic, cannot assume to be realistic.

### URBAN-SED

http://urbansed.weebly.com/

Syntetic, cannot assume to be realistic.

#### Other

https://dcase.community/challenge2023/task-sound-event-detection-with-weak-labels-and-synthetic-soundscapes 

Synthetic, cannot assume to be realistic.
