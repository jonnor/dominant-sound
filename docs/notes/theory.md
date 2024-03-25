
# Theory

## Single dominant source

Given a mixture of two sound sources, A and B, where A is the louder of the two.
If B is -5dB of A, then B contribution to sum is 1.2 dB
If B is -10dB of A, then B contribution to sum is 0.4 dB
This means that when A is +10 dB of B, its contribution to the sum is neglible.

The sum based on difference in dB level of two sources can be plotted on a curve which illustrates this.

## Strategies for detecting noise events

ACOUSTICS 2016.
Measurement of noise events in road traffic streams: Initial results from a simulation study


Category 1. Fixed threshold for noise event detection
Using a predefined value in dB SPL.
Typical values for this threshold have ranged from 45 dB(A) for identifying events
in indoor situations with closed windows to 80 dB(A) for detecting events in outdoor situations.

Category 3: Adaptive thresholds.
Events are detected when the instantaneous sound level emerges by a specified amount.
Typically 3 to 15 dB(A), above another conventional traffic noise indicator such as LAeq, LA50, or LA90.


## Thresholds for becoming noticable noise

TITLE 7 NATURAL RESOURCES & ENVIRONMENTAL CONTROL DELAWARE ADMINISTRATIVE CODE, 1149 Regulations Governing the Control of Noise. USA

> Intrusive noise means unwanted sound which intrudes over and above the existing noise at a given location.
> The relative intrusiveness of the sound depends upon its
> amplitude, duration, frequency, time of occurrence and tonal or informational content as well as the prevailing ambient noise level.
> A sound pressure level of 3 dB(A) above the ambient level is normally just discernable,
> with levels of 5 dB(A) to 10 dB(A) the lower level region for complaints.

Noise Guide for Local Government Part 2 Noise assessment, Australia

> The NSW Industrial Noise Policy (EPA 2000),
> which is specifically aimed at large and complex industrial activities,
> defines intrusive noise as 5 decibels above the background noise level
> 
> The background level is the LA90 measurement of all noise in the area of the complaint
> without the subject noise operating or affecting the measurement results.
> 
> The Interim Construction Noise Guideline (DECC 2009) notes there may be
> some community reaction to noise from major construction projects where this is more than 10 decibels
> above the background noise level for work during the daytime.
> This recognises that construction noise is generally temporary
> with the community having a slightly higher tolerance for it.

BS4142:2014 states

> The significance of sound of an industrial and/or commercial nature depends
> upon both the margin by which the rating level of the specific sound source exceeds the background
> sound level and the context in which the sound occurs
> ...
> A difference of around +10dB or more is likely to be an indication of a significant adverse impact,
depending on the context.”
> A difference of around +5dB is likely to be an indication of an adverse impact,
depending on the context.”


## Signal to Noise Ratio for sound events

A SNR calculation for sound events that can be used with dynamically varying background noise.

> The N central samples in the event period were the ones used to calculate the power of the signal,
> and the 𝑁/2 samples before and after the event were used to calculate the power of the noise

Described in
On the Impact of Anomalous Noise Events on Road Traffic Noise Mapping in Urban and Suburban Environments (Orga, Alías, Alsina-Pagès, 2018).
Also used in
BCNDataset: Description and Analysis of an Annotated Night Urban Leisure Sound Dataset (Vidaña-Vila, Duboc, Alsina-Pagès, Polls, 2020).

Seems a rather straightforward definition and method. Probably used in other places also?

Weakness: If immediately followed or preceeded by a louder event, will show negative.
Could maybe try to mask also surrounding (labled) events? To better estimate the "true" background?

## Impact of Sound Event on Leq

Impact is relative to the 5 min of 𝐿𝐴𝑒𝑞 measured surrounding the event.
To obtain the final impact value, the 𝐿𝐴𝑒𝑞 of the signal is obtained.
Then, the labeled event is removed and replaced by an interpolated value of the background noise to maintain a continuous energy of the signal.
Finally, the impact is measured as the subtraction between the initial 𝐿𝐴𝑒𝑞 and the 𝐿𝐴𝑒𝑞 without the labeled event.

Described in
BCNDataset: Description and Analysis of an Annotated Night Urban Leisure Sound Dataset 
and refers to
On the impact of anomalous noise events on road traffic noise mapping in urban and suburban environments

? This could be extended to entire classes of events?


## Traffic Noise Index
Langdon FJ, Scholes W.
The traffic noise index: a method of controlling noise nuisance.
Architects' J 1968; 147: 20.
https://files.eric.ed.gov/fulltext/ED035210.pdf

## Noise Pollution Level
Robinson DW. The concept of noise pollution level.
J Occup Environ Med 1971;


## Common Noise Index
Ribeiro C, Anselme C, Mietlicki F, Vincent B, Da Silva R, Gaudibert P (eds.)
At the heart of Harmonica project: the Common Noise Index (CNI)
6a Giornata di Studio sull’Acustica Ambientale 2013
https://www.bruitparif.fr/pages/En-tete/300%20Publications/680%20Articles%20scientifiques/2013%20-%20At%20the%20heart%20of%20Harmonica%20project%20%20-%20Genova.pdf

Proposed 5 different models by combining acoustic metrics.
Tested how these prediced noise annoyance levels.
Chose P2 as the Common Noise Index (CNI).
Consisting of a linear model of LA90, LA90-LA10, NEL55
NEL55 = Number of hourly events that break the 55 dB(A) mark


## Notice-events
De Coensel B, Botteldooren D, De Muer T, Berglund B, Nilsson ME, Lercher P.
A model for the perception of environmental sound based on notice-events.
J Acoustic Soc Am 2009; 126: 656–665.
https://www.academia.edu/download/49889749/A_model_for_the_perception_of_environmen20161026-29154-wb90de.pdf

## Fluctuation and emergence
Bockstael A, De Coensel B, Lercher P, Botteldooren D editors.
Influence of temporal structure of the sonic environment on annoyance
10th International Congress on Noise as a Public Health Problem (ICBEN) 2011. London, UK

## Summaries of acoustical indicators that go beyond continious sound level

I-INCE Publication Number: 2015-1
SUPPLEMENTAL METRICS FOR DAY/NIGHT AVERAGE SOUND LEVEL AND DAY/EVENING/NIGHT AVERAGE SOUND LEVEL
Final Report of the I-INCE Technical Study Group on Metrics for Environmental Noise Assessment and Control (TSG 9)
2015



## Intermittency ratio
Intermittency ratio: A metric reflecting short-term temporal variations of transportation noise exposure.
https://www.nature.com/articles/jes201556
Journal of Exposure Science & Environmental Epidemiology volume 26, pages 575–585 (2016)

150 citations

> Regarding noise effects on health and wellbeing,
> average measures often cannot satisfactorily predict annoyance and somatic health effects of noise,
> particularly sleep disturbances.
> It has been hypothesized that effects of noise can be better explained when also considering the
> variation of the level over time and the frequency distribution of
> event-related acoustic measures, such as for example, the maximum sound pressure level.

> For an integral characterization of the "eventfulness" of an exposure situation over a longer period of time
> we introduce the event-based sound pressure level Leq,T,Events,
> which accounts for all sound energy contributions that exceed a given threshold, that is, clearly stand out from background noise.
> This event-based sound pressure level Leq,T,Events can now be compared with the overall sound pressure level Leq,T,tot.
> The IR is defined as the ratio of the event-based sound energy to the overall sound energy.

> This threshold K is defined relative to the long-term average of the overall sound pressure level Leq,T,tot and an offset C
> On the basis of practical experience on transportation noise situations,
> C might not be smaller than 0 and not larger than about 10 dB. For low values of C
> ...
> To be able for IR to distinguish between situations with different degrees of intermittency,
> the criterion for setting C was a preferably uniform spread of IR across the range of exposure situations as they occur in the real world.
> The balance between these extreme cases was investigated by numerical simulations of various traffic situations and resulted in C=3 dB.

> Air and railway traffic generally exhibit a high IR,
> with the exception of situations with such a high background noise
> (e.g., noise from other sources) that the events are partially or fully masked.


> The question of how much an event really has to stand out from background noise in order to be termed "event"
> by normal listeners depends on various other parameters (which were not addressed in the present paper).
> In fact, for the noticeability of an event, not only the acoustic characteristics of the event compared to the background,
> but also the attentional, cognitive and emotional situation of the listener is relevant, as was described by de Coensel et al.
REF.
De Coensel B, Botteldooren D, De Muer T, Berglund B, Nilsson ME, Lercher P.
A model for the perception of environmental sound based on notice-events.
J Acoustic Soc Am 2009
https://www.academia.edu/download/49889749/A_model_for_the_perception_of_environmen20161026-29154-wb90de.pdf

Shows many plots with examples of soundlevel variation in scenarios of interest.
Ex railway and highway at night. 
Highway was 45-55 dBA. Railway was 30-65 dBA.


#### Road, Tram and Aircraft Traffic Noise Annoyance Related to the Number of Noise Events and the Equivalent Sound Level
https://journals.pan.pl/Content/125251/PDF/aoa.2022.142892.pdf
Based on listening tests

> Road, tramway, and aircraft traffic were investigated and two factors were manipulated:
> the equivalent sound level value and the number of noise events.
> ...
> The results showed that sound level is always a statistically significant parameter while
> the number of events has an impact only for tramways and airplanes.


#### Application of the Intermittency Ratio Metric for the Classification of Urban Sites Based on Road Traffic Noise Events 
https://www.mdpi.com/1424-8220/19/23/5136
2019

To have a more detailed characterization of noise exposure, IR, describing SPL short-term temporal variations,
has proved to be a useful supplementary metric accompanying LAeq,
which is limited to measure the energy content of the noise exposure.

> Road traffic noise is typically characterized by the noise events due to the single vehicle pass-by,
> where the temporal structure of SPL varies between local one-lane city roads,
> showing highly intermittent noise, up to wide multi-lane motorways,
> producing a nearly continuous noise with very limited SPL fluctuations.

#### A survey on exposure-response relationships for road, rail, and aircraft noise annoyance: Differences between continuous and intermittent noise
2019
https://www.sciencedirect.com/science/article/pii/S016041201831897X

- Noise annoyance is associated with Lden of road, rail, and aircraft noise exposure.
- The degree of intermittency of noise can explain differences in annoyance reactions.
-  the inclusion of the IR metric in the exposure-response model for %HA could explain differences of >6 dB between road traffic noise exposure situations with low (10%) or rather high (90%) IR24h
- predictive value of using IR in the modeling of %HA was less strong in the case of railway noise (Fig. 7)
- Finally, IR was not linked to aircraft noise annoyance after full statistical adjustment



## Regulations / Guidelines etc

WHO Guidelines for Community Noise (1999)
Dwelling, indoors. Sleep disturbance night time. 30 dB LAeq, 45 dB LAFMax
Outside bedrooms. Sleep disturbance, window open (outdoor values). 45 dB LAeq, 60 dB LAFmax
From noise sources other than road traffic, railways, aircraft or wind turbines

City of Westminister
Draft Noise Technical Guidance Note (September 2020)
https://www.westminster.gov.uk/sites/default/files/ev_env_005_v2_noise_technical_standards_wcc_september_2020.pdf

> Inside bedrooms 45 dB LAFmax to be exceeded no more than
> 15 times per night-time
> from sources other than emergency sirens.

Example of guideslines in Leeds
https://www.leeds.gov.uk/planning/planning-policy/supplementary-planning-documents-and-guidance/noise-and-vibration-planning-guidance

