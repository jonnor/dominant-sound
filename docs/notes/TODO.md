
# Context

Our primary resource questions are

1. How often is the single-dominant-source-at-a-time a reasonable assumption?
2. How well can we attribute soundlevels to their class?
3. How well can we automate this using Sound Event Detection

Details are in the research plan.

# Checkpoints

- Are we able to answer our questions (well enough) with current data?
Assume yes for now. Revisit in March 24.
- ?

# Access to expertice

- Ask Dag. Ask OJ for budget.

# 1. Single dominant assumption

#### Time-attribution
How much of the time can we explain?
Time-period.

#### Noise-level attribution
How much of the overall soundlevel/noise level.

#### Open questions

- EDA. How much of the audio is annotated?
Remaining is "unknown" class. How much is it in terms of LEQ/SEL?
- EDA. Co-occurence of events. Mixed class

#### Misc

- Extract sparse events (start, end) from delta soundlevels, based on thresholding
- Move analysis into a .py module
- Run analysis in CI

# 2. Soundlevel attribution


# 3. Sound Event Detection

- Fixup the SED pipeline. python -m src.sed.train
- Addd SED pipeline to CI
- Evaluation in terms of precision/recall
- Evaluation in terms of dB error

# Paper

Most TODOs are tracked inside the paper itself

Overall steps

- All plots/tables ready
- All surrounding sections ready. Introduction,Background,Acknowledgements
- Core sections ready. Methods,Results,Discussion/Conclusions
- Re-write abstract to fit the contents/findings
- Ready for internal review


