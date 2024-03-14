
# Related work


### Road Traffic Noise vs Anomalous Noise Event
Being able to separate Road Traffic Noise from other noise events has been studied,
and methods for this proposed and discussed in:

Development of an anomalous noise event detection algorithm for dynamic road traffic noise mapping
https://www.researchgate.net/publication/272784654_Development_of_an_anomalous_noise_event_detection_algorithm_for_dynamic_road_traffic_noise_mapping
ICSV22, 2015
Road Traffic Noise (RTN) versus other, Anomalous Noise Event (ANE)
! almost only self-citations.

Methods for Noise Event Detection and Assessment of the Sonic Environment by the Harmonica Index 
https://www.mdpi.com/2076-3417/11/17/8031 
2021
Discusses different noise event indicators.

> 2.2.2. Recognition of the Noise Event Source
> ANED algorithm was trained using more than 150 h of expert-manually labeled data,
> coming from the 24 sensors, deployed by the DYNAMAP project in Milan, with around 8% of anomalous noise events
> (e.g., bird singing, sirens, dogs barking, horns, trams)

Development and validation of an anomalous noise events detector focused on salient events through an urban and suburban WASN adapted to real-operation
https://merit.url.edu/ca/publications/development-and-validation-of-an-anomalous-noise-events-detector--4
ICSV 2021
Road Traffic Noise RTN vs Anomalous Noise Event (ANE).

> The algorithm detected — for the events catalogued as high-salience:
> — all of the present airplane noise
> - more than 90% of works, and people talking
> 
> For the mid-high salience
> - more than 84% of airplane noise
> - nearly 80% of works
> - and more than 60% of people talking


On the Impact of Anomalous Noise Events on Road Traffic Noise Mapping in Urban and Suburban Environments
F Orga, F Alías, RM Alsina-Pagès
2018

> This paper introduces an analysis methodology considering both Signal-to-Noise Ratio (SNR)
> and duration of ANEs to evaluate their impact on the A-weighted equivalent RTN level calculation for different integration times.
> The experiments conducted on 9 h of real-life data from the WASN-based DYNAMAP project
> show that both individual high-impact events and aggregated medium-impact events
> bias significantly the equivalent noise levels of the RTN map
> making any derived study about public health impact inaccurate


# Sound Event Detection

#### Cosmopolite Sound Monitoring (CoSMo): A Study of Urban Sound Event Detection Systems Generalizing to Multiple Cities

https://ieeexplore.ieee.org/abstract/document/10095833
Tests SED on SONYC-USD and SINGA:PURA datasets.

Investigates performance wrt low-high polyphony (overlapping sounds), and "near" vs "far" poximity/salience.

Compares CRNN with OpenL3 and PaSST embedding classifiers.
Says OpenL3 performs better in mismatched scenarios.

https://github.com/kkoutini/PaSST
has 0.46-0.47 mAP on AudioSet vs 0.44 for CNN14 from

### Environmental noise monitoring using source classification in sensors

https://trepo.tuni.fi/bitstream/handle/10024/126273/Environmental_noise_monitoring_using_source_classification_in_sensors.pdf
2018

Tested at rock crusher site
