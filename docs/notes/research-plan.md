
# Task formulations

## Dominant Sound Classification

TLDR: Modification on (closed-set) Audio Classification,
where the output class shall be the one that contributes the most to the soundlevel.

Input

> Stream of audio. Consisting of sound events from multiple different sound sources.

Output

> Single class label. Being the class that contributed the most to the soundlevel.

## Dominant Sound Event Detection

TLDR: Modification on (monophonic) Sound Event Detection,
where the output class shall be the one that contributes the most to the soundlevel.

Input

> Stream of audio. Consisting of sound events from multiple different sound sources.

Output

> A stream of class activations over time one per point in time.
> The active class shall be the one that made the most contribution to the soundlevel.
> High resolution at output, corresponding with soundlevel measurement. For example LA_fast (125 ms) or LA_slow (1000 ms).

## Common
In addition to `{class0,class1....classN}`, also allow for two pseudo-classes: {unknown,mixture}

- `unknown` means the model cannot reliably detect the class.
- `mixture` means that the dominant-source assumption is violated,
there are multiple sources that meaningfully contribute to the overall noise level.


# Research questions

- How often is the single-dominant-source-at-a-time a reasonable assumption?
- How well can we attribute soundlevels to their class?

# Hypothesis

The big stuff

- The Dominant Sound assumption holds a lot of times in real Noise Monitoring usecases
- Using the Dominant Sound assumption simplifies analysis, and enables useful Noise Monitoring metrics
- Dominant Sound Classification can be done with standard Audio Classification methods,
given an appropriately labeled dataset.
- Dominant Sound Event Detection can be done with standard Sound Event Detection methods,
given an appropriately labeled dataset.

Small things that would be good to figure out

- Applying the same frequency weighting curve used for soundlevel to the spectrogram used for classification,
makes it easier for models to solve the Dominant Sound Classification / Sound Event Detection task.
At least with limited data and/or model capacity.

# Overall research agenda

Goal: Use Machine Learning to provide useful information about noise source/cause

Overall problem statement

- How to use ML to automaticaly analyze the audio to extract useful information,
and to realize practical noise monitoring systems, that can do this efficiently?

Sub-questions

-- How to combine noise indicators level with ML derived parameters?
-- What are the limitations and weaknesses of current ML approaches in getting usable information?
-- Which sub-problems are solvable with technology available today (and which are not)?
-- How to aggregate the information to a meaningful level?
-- How to present the data in a way that makes it useful?
-- How to achieve positive impact using the information? Reduction in annoyance and health risks.

Hypothesis. Instrusive events (high salience, high SNR) are more solvable than general case.
Hypothesis. Single source attribution simplifies presentation of information.
Hypothesis. ML methods that are not soundlevel aware may misclassify the relevant source.

# Research methods

## How often is the single-dominant-source-at-a-time a reasonable assumption?

Or v.v., how often is the single-dominant-source-at-a-time assumption broken?
How often does two (or more) noise sources appear concurrently, where B is within 10 dB of A
Time resolution either 125ms (LAF) or 1 second (LAS).

#### Possible ways of answering

- Analysis of selected recordings in representative scenarios. Qualitative
- Statistical analysis of co-occurence, given simple models
- Analysis of real-world dataset covering many cases. Primarily quantitative

#### Simplified statistical analysis of co-occurrence

For example:
Given two noise sources, each active for 5 seconds at a time.
Say 30 seconds between each activiation.
Assume that they are independent from eachother.
What is probability of happening at same time?
ie overlapping by 1 second or more.
Model emission with Poisson?

Two variables: duration and period between events.
Can compute probabilities of co-occurence as a table.

#### Small scale analysis

Pre-requisites: Identify some appropriate scenarios.

Could maybe select some time-periods
Say 10-30 seconds long
that are representative of whole dataset
analyze these manually
mark periods of single dominant, multiple contributions

#### Large scale analysis

If one can get/produce sufficient labeled data,
then can go straight for a Sound Event Detection problem.


If one had captured a mixture of these things, but without a lot of labels.
Might need to do a statistical and/or generative analysis.

statistical analysis
each source modelled as a soundlevel generating process
characterized by
a. sound level distribution
LAFeq for each time-step
b. emission probabilities


## How well can we attribute soundlevels to their class?

Measure in terms of dB. Ground truth computed from labels.
Requires a labeled dataset with suitable labels.

Purpose is to demonstrate this methodology and its usefulness,
so performance does not need to be super high.
Hopefully able to stay with simple and well-understood deep learning baselines.

#### Using Sound Event Detection

Supervised learning.
Need strong labels. Both for training of SED model.
But especially for evaluation of dB attribution.

#### Evaluation

How much of the "dB" can the model (correctly) explain?
What would it be assuming perfect detection (upper boundary of performance).
In only the intrusive events (Leq contribution, percentage of LAFmax), and overall (contribution to Leq).


#### Feature representation

Using a time-frequency (spectrogram) representation as the input.
Maybe try to A-weight the spectrogram.

Using off-the-shelf detection models.
As vanilla training setup as possible.



Candidates

* CRNN like SEDNet a good baseline. https://github.com/sharathadavanne/sed-crnn
* CRNN also described in Sound Event Detection: A Tutorial, https://arxiv.org/abs/2107.05463


# Open questions
Things that need to be resolved to answer hypothesis or parts thereof.

## Noise Monitoring scenario/usecase
Which usecase are a good fit of the proposed method?

Method benefits scenarios where there are multiple noise sources,
and where discriminating between them is of interest,
particularly were it is useful to be able to "assign" each noise to a class.

In general, for measurement of human-created noise, we would like to separate out
Biophony and Geophony from Anthrophony.
Ref Soundscape Ecology.

Noise regulations tend to regulate based on noise sources.
In a mixed-environment, such as residential, multiple.
Road Noise vs Air Traffic vs Rail Noise vs Industrial vs Community vs Other.

Two types of uses:

A) Being able to do overall analysis of a soundscape/situation.
Over longer periods of time, say 1 week or more.
Need method to be unbiased.
Primarily on an aggegated/statistical level, not necessarily every single minute.

Compare per-class event counts, in aggregate
Compare per-class LAeq contribution, in aggregate

B) Being able to attribute particular (periods of) noise events to a source/class.
Need to have high precision for such events. And sufficient recall to actually be able to attribute, not just have "unknown".


## Choice of classes
Find and use established taxonomies/ontologies.
Preferably from the noise/acoustics area.
Or if not found, from audio machine learning area.

## Choice of datasets
Assuming that large-scale analysis is done.
Do appropriate datasets exist at all?

# Limitations

#### Ignoring of short-time temporal characteristics 
Each activation of a source has a short (soundlevel) sequence associated with it.
Assuming that LAF/LAS captures well enough.


# Notes

Considering the BCN dataset
Impact of each sound event on Leq beem to be very small?
Most events, even with delta over +5 dB have estimated impact on 1 minute Leq under 0.01
!? is this even correct. TODO: add some unit test?
Depends probably a lot on duration of event. And loudness.

Understanding the events.
Maybe plot event soundlevels from many events, on top of eachother.
Using grey before+after to indicate relation to background/other sounds?
Have plot_clip_sections starting point for this

## Event co-occurrence

Event co-occurence
How often does it happen based on the annotations?
If using an analysis window approach, depends on window length
For a typical audio classifier model, would be around 1 second

Multiple possible defintions

- Events of any class.
- Events from different coarse classes
- Events from different fine grained classes

On BCN dataset seems to be around 8% of the time for 1 second windows on the original classes
1846 out of 21832 seconds. Using non-overlapping windows.

This could be enough for a test set?
For example for detecting "mixed".
Or checking that loudest is being returned.
Comparing own approaches to pretrained etc

There are 3 files.
Could use them as train/test using leave-one-out cross-validation?

How much is going in terms of sound/noise level on in these events?
A bit more than for non annotated.

Verified visually that the picked out events do have the correct labels categories.
none/single/multiple


# Ideas

## How well can pre-trained models classify the dominant sound source?

Synthesize mixtures.
Consisting of
1) background noise
2) event A
3) event B

Difference between levels of event A and B are varied. From for example -12 dB(A) + 12 dB(A)
Check which class the output is. Check if the louder sound is the one picked.

Also vary the difference between levels and background levels?
Event levels being +0 dB to +20 dB LAeq.

Do this for a large set of event classes.
See if there are certain events classes or pairs where misclassifications are common.

Background should be? White noise? Babble noise? Or real soundscapes (that are relatively constant)?

For each analysis window.
Of ~1 second, as is common with pretrained models.

Pretrain model examples. YAMNet, PANNs, OpenL3, PaSST. Trained on AudioSet.

Research question: Can pre-trained models be used to classify (dominant) noise source?
Hypothesis.
No, not as-is. There will be types of sound where class probability is not connected to loudness.
As-is do not have a way to separate just background or mixed scenarios.
Can it be retrofitted based on the class probabilities? Or basic pre-filtering on the soundlevels?

Try to pre-filter the audio/spectrograms with A weighting. See if this improves performance
Try to train with targets that are the dominant sound.



## Synthetic datasets

Can synthesize mixtures to form a dataset.
Different dB ratios of A,B (might also need to have background noises C,D,E)
Train model to recover the dominant event. Or maybe to predict the dB ratio.
Should be powerful as a pre-training concept, to get large training sets, which should enable strong models.
Possible target for a follow-up paper.

## TinyML classification

The Dominant Sound Event Detection task should be solvable using SED systems that
can run on contemporary IoT Noise Monitoring devices.
Target for a follow-up paper.

## Generative modelling

Might be possible to have source activity as a binary ON/OFF.
Maybe the activation patterns of sources can be Poisson

Could we formulate a generative model,
and fit it to real-world mixtures?
could test it on synthetic mixtures first,
to check if model is able to fit properly.

Target for follow-up paper.
Unless critical to answer the hypothesis above.

