# Task 05 — Descriptive Statistics and Large Language Models

*From ground truth to LLM judgment.*

This repo documents an experiment: I computed trustworthy descriptive statistics
for a small dataset using my own verified code, then interrogated a large language
model about that same data in natural language and checked every answer against my
ground truth.

> Fill in every section marked **TODO** with what you actually did and observed.
> The grade rests on honest documentation of the real experiment, not on a clean
> success — a well-documented model failure counts just as much.

## The dataset

- **Source:** Syracuse University Women's Lacrosse — 2026 cumulative statistics,
  https://cuse.com/sports/womens-lacrosse/stats/2026
- **What it is:** One full season (2026) of Syracuse Women's Lacrosse team
  statistics, extracted from the official cumulative-stats PDF into two CSVs:
  - `players.csv` — per-player totals (GP, G, A, PTS, SH, GW, GB, DC, TO, CT, FOULS).
  - `games.csv` — per-game results (Date, Opponent, WL, SU_Score, Opp_Score).
- **Size:** 33 players, 20 games (14-6 overall record).
- **Quirks / quality notes:**
  - A "TM Team" row appears in the PDF with team-level TO (13) and DC (2) that
    don't belong to any individual — skipped during analysis.
  - Several players (goalies, reserves) have GP ≤ 5 and all-zero offensive stats.
  - Draw controls (DC) for Guzik (#22) is 73 — unusually high, appears correct
    per the source PDF.
  - One player name has a trailing space in the PDF ("Hodges , Savannah").
  - No SOG column in the cumulative stats; shot-on-goal data exists only in the
    aggregate team-stats section of the PDF.

**The data files are NOT in this repo** (per the assignment). To reproduce:
download the two tables from the page above, save them as `data/players.csv` and
`data/games.csv`, then run the ground-truth scripts below.

## Reproducing the ground truth

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # not needed for the pure-Python script
python pandas_stats.py data/players.csv
python pandas_stats.py data/games.csv
```

These are the descriptive-statistics scripts from the earlier tasks; they are my
answer key. Additional analysis scripts:
- `metrics.py` — computes the Game Changer index, offense-vs-defense lever, and
  the "one player to develop" recommendation. See `METRICS.md` for definitions.

## The experiment — narrative

### Phase A — baseline factual Q&A
TODO — Which model(s) and version(s) you used. How you supplied the data (raw CSV,
markdown table, pasted summary). The arc of what you asked and what happened. Point
to `prompt_log.md` for the full record.

### Phase B — derived metrics and judgment
TODO — The metric definitions you wrote (see "Metrics" below). How prompt
engineering moved the model from weak to defensible answers. The advisory "coach"
question and whether the recommendation survived your validation.

## Metrics I defined (Phase B)

Full formal definitions are in [`METRICS.md`](METRICS.md). Summary:

1. **Most Improved Player** — largest positive Δ in points-per-game between the
   first and second half of the season. *(Not computable from cumulative stats;
   requires per-game box scores.)*
2. **Game Changer** — composite z-score of three per-game rates (offense = Pts/GP,
   possession = DC/GP, disruption = (GB+CT)/GP), equally weighted, for players
   with GP ≥ half the team's games.
3. **Offense vs. Defense Lever** — compare the scoring shortfall and conceding
   shortfall in close losses (lost by 1–2 goals) against season baselines;
   the larger shortfall names the lever.
4. **One Player to Develop** — if offense lever, pick a top-GameChanger player
   with high shot volume but below-median shooting %; if defense lever, pick
   the DC/GP or CT/GP leader.

## Where the model succeeded and failed

TODO — Your honest findings. At what question/column/context size did accuracy
break down? Was it confidently wrong? Did forcing code execution help? Where would
you trust an LLM with real analytical work, and where would you insist on checking?

## Files

| File | Purpose |
|---|---|
| `prompt_log.md` | Ordered log of every prompt, response, and verdict. |
| `METRICS.md` | Formal definitions of Game Changer, Lever, and development-pick metrics. |
| `metrics.py` | Standalone script that computes all metrics from the CSVs. |
| `pure_python_stats.py`, `pandas_stats.py`, `polars_stats.py` | Ground-truth scripts (reused). |
| `requirements.txt` | Dependencies. |
| `figures/` | Any visualizations the model produced (clearly named). |
| `.gitignore` | Keeps `data/` and CSVs out of the repo. |
