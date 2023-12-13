
## Format
Abstracts of up to 200 words

## Submission
www.icsv30.org

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


## Straight

Propose a method for noise monitoring that can automatically determine the soundlevel contribution
of noise events coming from different noise sources.
This stems from the observation that in some monitoring cases t
This enables a simplified approach to attributing soundlevel contributions to,
where at each single time-instant it can be assigned to a single event class.

Our contribution is 
A) formalization of two Machine Learning tasks designed to consider the soundlevel contribution during classification, 
called: Dominant Sound Classification and Dominant Sound Event Detection.
B) Evaluation of to which degree the dominant sound simplification holds in noise monitoring scenarios
C) Demonstration of a complete system to attribute soundlevel contributions to noise sources, and evaluation of its performance


## Keywords

Dominant Sound Event Detection

Tools to automate analysis of noise

## Music

Our aim is to use machine learning to categorize the audio stream,
and to automatically determine the contribution that each class has to the soundlevel.

