
# Context

Our primary resource questions are

1. How often is the single-dominant-source-at-a-time a reasonable assumption?
2. How well can we attribute soundlevels to their class?

Details are in the research plan.

## Single dominant assumption

- Merge stereo audio into single-channel
- EDA. Durations of events
- EDA. Co-occurence of events. Mixed class
- Create curated combined data frames. Designed for analysis format
- Move analysis into a .py module
- Run analysis in CI
- Plotting tools that combine spectrogram,soundlevel,annotations (and prediction)


## Soundlevel attribution

- Setup basic SED pipeline
- Estimate best-possible levels from annotations
- Evaluation in terms of precision/recall
- Evaluation in terms of dB error

## Paper

Most TODOs are tracked inside the paper itself

Overall steps

- Get all plots ready
- Ready for internal review

## Reproducability

- Setup Github Action that downloads data and runs pipeline
