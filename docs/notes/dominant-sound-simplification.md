## Overview
This document is to formalise the methodology for Part B of "our contribution", *Evaluation of to which degree the dominant sound simplification holds in noise monitoring scenarios*

Dominant sound simplification: The assumption that a noticeable sound event (+5dBA over LA90/Background) can be attributed to a single "dominant" source.

Noise monitoring scenarios: 
- Noise sensitive buildings (Schools, hospitals, particular commercial/industrial facilities)
- Noisy industrial activity (Construction, demolition, explosives, heavy plant/machinery)
- Noisy community activities (Pubs, clubs, bars, festivals)
- Noisy transportation activities (Road, rail, aircraft)
- Military/defence and security (Intrusion detection, asset/facility monitoring)

Benefits of this contribution:
- The goals of noise monitoring are; 1) To quantify/count the rate/number of sound events at a location, and 2) to attribute those events to a particular source.
- If the "dominant sound simplification" holds true, it should be possible to classify the source of each sound event with a standard neural network classifier.
- If the "dominant sound simplification" doesn't hold true all the time (sound event with two or more dominating sources), it may still be possible to determine the level of contribution each source has towards the sound event.
- Either way, understanding the degree at which this assumption holds true will allow us to develop/design a method for automatically classifying sound events.

For example:
- Sound levels are monitored, sound events are detected with a sound event filter.
- If the simplification holds true, we can infer the source by running inference on the "event" with a standard classifier.
- If it doesn't hold true, we can apply "single/dominant" and "mixed" pseudo-classes when labelling training data to help the network understand these differences.


## Methodology

### Evaluation dataset
MAESTRO Real: A collection of 49 real-time recordings (3 to 5 minutes in length) from 5 scenarios:
1) Cafe/Restaurant (10 recordings)
2) City Center (10 recordings)
3) Grocery Store (9 recordings)
4) Metro Station (9 recordings)
5) Residential Area (11 recordings)

### Sound Event Detection/Filter
This filter marks the moments when the A-weighted soundlevel exceeds +5dBA over the "background" level (LA90).

#### Step 1) Apply A-weighting to the soundlevels
INPUT: Audio file

PROCESSING: Audio is parsed with the "soundlevel_for_file()" function.

OUTPUT: Dataframe containing N arrays of A-weighted soundlevels for N channels in the audio

#### Step 2) Compute rolling background levels (LA90)
INPUT: A-weighted soundlevels, window size (number of samples/frames to compute L90 over)

PROCESSING: 
1) Function, "compute_ln(n=90)" is called at each frame over the interval "frame_n" : "frame_n + window"
2) The returned array is padded with 0.5*window_size nans to the left

OUTPUT: An array of rolling L90 values with length equal to the length of dBA levels

#### Step 3) Filter for sound events and save timestamps
INPUT: Arrays of dBA levels and L90 values

PROCESSING:
1) Calculate the difference between dBA and L90 at each frame (dBA-L90)=diff
2) Fetch the indices where diff > threshold
   - *Thresholds of +5 and +10 were applied to help with labelling.*
3) Save timestamps to tab separated txt file with format [start \t end \t label]

OUTPUT: Txt file ready for importing to audacity


#### Step 4) Listen and label sound events
INPUT: Original audio file and txt file from step 3

PROCESSING:
1) Import audio file and label file to audacity.
2) Mix down audio file to mono.
3) Create a new label track and label the detected events.
4) Export labels.

OUTPUT: Txt file with Sound Event timestamps and manually labelled timestamps.


#### Step 5) Calculate proportion of sound events which are mixed vs. single source [*** Not started this process yet***]



## Things I might have got wrong, need some clarification

1) Rather than mix down the two channels of levels returned by *soundlevel_for_file()*, I only used channel 0 for the rest of the steps. Should I first be combining the two channels? If so, is it simply a matter of taking the mean at each step?
2) For step 2, I feel like we're calculating L90 from the future rather than the past. Eg, at step 0, I'm calculating L90 over step 0 to step0+window. I know we shift it over to account for that... but I just want to double check with you???
3) LAF and LAS; I know these are "fast" and "slow" levels, however I'm wondering where and how I should be incorporating these into my analysis?
4) When labelling sound events, is it strictly necessary to label "what" the sound is (eg, car), or is it enough to simply label "single" or "mixed"?
5) Identifying "Sound Events"... Is a one-frame spike over +5dB sufficient to class as a "sound event"? If not, should I be looking for "x consecutive frames over +5dB"? Is x related to the "fast" and "slow" resolutions?
