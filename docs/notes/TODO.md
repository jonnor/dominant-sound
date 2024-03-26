
# Context

Our primary resource questions are

1. How often is the single-dominant-source-at-a-time a reasonable assumption?
2. How well can we attribute soundlevels to their class?
3. How well can we automate this using Sound Event Detection

Details are in the research plan.

# Checkpoints

**CHECKPOINT**
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
How much of the overall soundlevel/noise level can we account for?

- Plot aggregated impact over entire clips
- Investigate overall impact. Check if the explanations make sense
- Try to compute SPL using the sensitivity values given

#### Open questions

#### Misc

- Move analysis into a .py module
- Run analysis in CI

# 2. Soundlevel attribution


# 3. Sound Event Detection
How much of the events can we detect automatically?
Can we get high performance on the most noticable/salient events?

- Check if we can get away with 1 second window.
Seems OK. There is some mixed sounds in such a small period, but not that much. Approx 8% on BCN.
If we can correctly 
Use masking of the times to estimate how much each contributes?

- Add feature extractors with pretrained AudioSet type models. YAMNet/PANNs, PaSST ?
- Fixup the SED pipeline. python -m src.sed.train
- Add SED pipeline to CI
- Evaluation in terms of precision/recall
- Evaluation in terms of dB error
- Implement SNR event metric. Compute for all labeled events
- Plot precision/recall vs SNR / impact

Challenge: Limited dataset. Single location.
Cannot really establish generalized performance. Danger of overfitting.

Possible strategy.
Use only a limited amount of labels for train/validate. Test on remainder.
Emulate a site-specific classifier setup. Where we can label some data.
Random selection. Select from the start. Select from the back.
N regardless of class. Or stratify.
!! do not knowN per coarse class. N per fine class. !! do not n
Use pretrained networks. From AudioSet. YAMNet/PANNs/PaSST.
Embeddings. Simple classifier. Linear/KNN/Simple RNN.

# Paper

Most TODOs are tracked inside the paper itself

Overall steps

- All plots/tables ready
- All surrounding sections ready. Introduction,Background,Acknowledgements
- Core sections ready. Methods,Results,Discussion/Conclusions
- Re-write abstract to fit the contents/findings
- Ready for internal review


