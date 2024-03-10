
## Format
Abstracts of up to 200 words

## Submission
www.icsv30.org

## Title

The Dominant Noise Event method for automatic classification in noise monitoring

## Theme

T10 - Signal processing and nonlinear methods
T10 RS03 - Signal processing in acoustics and vibration

## Keywords
Noise Monitoring, Machine Learning, Sound Event Detection

## Abstract

https://docs.google.com/document/d/1P2qKccu7TSv8tBmP852gNEoVkeueLZHOTu-1mcGc9yQ/edit

We propose a method for noise monitoring that can automatically classify noise events
and determine the sound level contribution from different noise sources. We observe that in some noise monitoring scenarios, the main phenomena of interest are intrusive noise events, which are considerably louder than the background.
When the noise events dominate the background level, it is possible to assign the sound level contribution at each time-period to a single event class.

Our contributions are
A) a formalization of two Machine Learning tasks designed to consider the sound level contribution during classification, tenatively called: Dominant Sound Classification and Dominant Sound Event Detection.
B) an analysis of to which degree the dominant sound simplification holds in noise monitoring scenarios
C) a demonstration of a complete system that attributes sound level contributions to noise source classes

The method is evaluated quantitatively using representative real-world datasets.


## Summarized
Linear, starting with background, building up the case step by step.
A bit boring. Long time until the contribution the paper comes in.

The availability and cost of Noise Monitoring systems that can measure soundlevels
over longer periods of time are decreasing steadily.
Recent research has also shown that it is possible to use Machine Learning 
to automatically classify audio clips and sound events.
However there is still a lack of tools and methodologies that combine the results
of high-resolution soundlevel monitoring with automated classification,
in order to create automated noise monitoring systems that can quantify
how different sound sources contribute to the overall noise impact.

A perfect solution would require the ability to perform source separation for each class of interest,
which is extremely difficult in the general case (underdetermined mixture, low signal-to-noise ratio).
We observe that noticable noise events are the main phenomena of interest in several noise monitoring scenarios.
Such events are considerably louder than the background noise,
and in short time-spans the soundlevel of the event may dominate the soundlevel of the background.
It may be thus possible to assign the soundlevel only to the class of the noise event,
meaning that a classification/detection approach rather than source separation can be used.

We propose a method for measuring soundlevels following this principle,
using a standard neural network architecture for Sound Event Detection. 
We explore to which degree the dominant sound-source simplification holds in selected noise monitoring scenarios,
and how much of the overall noise impact can be quantified using this method.
Evaluation is done on real-world datasets that are representative of noise monitoring scenarios.



## Notes

Dominant Sound Event Detection

Tools to automate analysis of noise

## Misc

Our aim is to use machine learning to categorize the audio stream,
and to automatically determine the contribution that each class has to the soundlevel.

