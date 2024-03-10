## Overview
This document is to formalise the methodology for Part B of "our contribution", *Evaluation of to which degree the dominant sound simplification holds in noise monitoring scenarios*

Dominant sound simplification: The assumption that a noticeable sound event (+5dBA over LA90/Background) can be attributed to a single "dominant" source.

Noise monitoring scenarios: 

- Noise sensitive buildings (Schools, hospitals, particular commercial/industrial facilities)
- Noisy industrial activity (Construction, demolition, explosives, heavy plant/machinery)
- Noisy community activities (Pubs, clubs, bars, festivals)
- Noisy transportation activities (Road, rail, aircraft)
- Military/defence and security (Intrusion detection, asset/facility monitoring)

The goals of noise monitoring are;

1) To quantify/count the rate/number of sound events at a location
2) to attribute those events **and their soundlevel contribution** to a particular source.

The approach proposed here

A) When "dominant sound simplification" holds true,
it should be possible to classify the source of each sound event as a single source.
A neural network classifier using the monophonic "Sound Event Detection" can be used.

B) When "dominant sound simplification" doesn't hold true (sound event with two or more dominating sources),
then a monophonic Sound Event Detection approach cannot be used.
Instead a Source Separation approach would be needed.
OUT OF SCOPE.

Understanding the degree at which this assumption holds true will
allow us to develop/design a method for automatically classifying sound events.


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


#### Step 5) Calculate proportion of sound events which are mixed vs. single source
[*** Not started this process yet***]



## Things I might have got wrong, need some clarification

### 1) Multi-channel
Q: Rather than mix down the two channels of levels returned by *soundlevel_for_file()*,
I only used channel 0 for the rest of the steps. Should I first be combining the two channels? If so, is it simply a matter of taking the mean at each step?

A: We should probably combine stereo recordings into one channel.
This is best done in the audio space, before soundlevel and spectrogram calculations.

### 2) Background estimation

Q: For step 2, I feel like we're calculating L90 from the future rather than the past.
Eg, at step 0, I'm calculating L90 over step 0 to step0+window.
I know we shift it over to account for that...
but I just want to double check with you???

A: As long as the timestamp for the calculated window is at the end of the window, that is OK.

### 3) ~~LAF and LAS
Q: I know these are "fast" and "slow" levels, however I'm wondering where and how I should be incorporating these into my analysis?

A: Both are used in the industry.
Sometimes the particular choice to use is specified in regulations, standards, procedures or guidelines.
Both are simplifications with tradeoffs between ability to quantify a peak, and the "integrated" sound level over a bit of time.
The choice *may* (or may not) influence our results.
This information may in itself be considered a research finding.
So **I think we should try both, and see if there are any noteworthy differences**.

### 4) Labeling strategy
 
Q: When labelling sound events,
is it strictly necessary to label "what" the sound is (eg, car), or is it enough to simply label "single" or "mixed"?

Discussed on Slack.
Each event is labeled with the class.
"Mixed" is then a computed class. Where there are multiple overlapping labels in time with different classes.

### 5) Criteria for "Sound Events"

Q: Is a one-frame spike over +5dB sufficient to class as a "sound event"?
If not, should I be looking for "x consecutive frames over +5dB"?

There are many reaonsable definitions.
But one needs to make a choice and stick too it.
Lets say yes to keep things simple - otherwise we get yet another parameter to select :D
There are already many choices baked in:

- Use of A frequency filtering for soundlevel.
There are other loudness models, more perceptual / more complicated.
- Use of Fast or Slow time integration for soundlevel
- Method for estimating background level / separating out events.
Just soundlevel (ignoring frequency spectrum changes).
Quantile type summarization, and specific quantile level, lookback window duration.
- Threshold level used (+5 dB etc)

Q: Is x related to the "fast" and "slow" resolutions?~~

A: Changing time integration already influences sensitivity of (relatively abrupt) sound events.
The same sound event will get reduced level when time integration is longer.

