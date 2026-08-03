
# BJJ Physical Training Engine v2

A multiple-choice, rule-based Streamlit app for apparently healthy adult Brazilian jiu-jitsu practitioners.

## What v2 adds

- BJJ and hard-sparring day selection
- Available physical-training day selection
- Automatic weekly placement of Strength A, Strength B, and Conditioning
- Session-duration trimming
- Exercise-by-exercise rationale and alternatives
- Four-week progression
- Weekly feedback and automatic next-week adjustment
- CSV downloads
- Safety stop rules

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Main engine flow

1. Safety screening
2. BJJ training-load estimate
3. Goal classification
4. Schedule constraints
5. Recovery classification
6. Session-template selection
7. Exercise-pool filtering
8. Sets, reps, RIR, and rest prescription
9. Weekly placement
10. Four-week progression
11. Weekly feedback adjustment

## Important boundary

This is an educational prototype, not a medical device. It does not diagnose, treat, rehabilitate, or clear a user for sport.

## Evidence note

The cited literature supports broad training principles. It does not validate every exact threshold, score, or exercise choice in this prototype. Those rules are intentionally transparent so they can be reviewed, tested, and version-controlled.
