
# Context

Our primary resource questions are

1. How often is the single-dominant-source-at-a-time a reasonable assumption?
2. How well can we attribute soundlevels to their class?

Details are in the research plan.

## Single dominant assumption

- Convert annotations to a single-track multi-class representation
- Extract sparse events (start, end) from soundlevels, based on thresholding
- Convert annotations to dense multi-track representation. Fix existing function
- EDA. How much of the audio is annotated?
Remaining is "unknown" class. How much is it in terms of LEQ/SEL?
- EDA. Co-occurence of events. Mixed class
- How much of Leq is explained?
- Group events into coarser classes
- Move analysis into a .py module
- Run analysis in CI
- Plotting tools that combine spectrogram,soundlevel,annotations (and prediction)


## Soundlevel attribution

- Fixup the SED pipeline. python -m src.sed.train
- Addd SED pipeline to CI
- Estimate best-possible levels using annotations
- Evaluation in terms of precision/recall
- Evaluation in terms of dB error

## Paper

Most TODOs are tracked inside the paper itself

Overall steps

- All plots/tables ready
- All surrounding sections ready. Introduction,Background,Acknowledgements
- Core sections ready. Methods,Results,Discussion/Conclusions
- Re-write abstract to fit the contents/findings
- Ready for internal review

## Reproducability

- Setup Github Action that downloads data and runs pipeline



