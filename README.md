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
- **What it is:** TODO — one season of team stats. Two tables captured as CSVs:
  - `players.csv` — per-player totals (GP, G, A, PTS, SH, GW, GB, DC, TO, CT, FOULS).
  - `games.csv` — per-game results (date, opponent, SU score, opp score, W/L).
- **Size:** TODO — N players, M games.
- **Quirks / quality notes:** TODO — e.g. a "TEAM" row, totals row, blank cells,
  goalie-only rows with no goals, etc. Note anything that could trip a reader.

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
answer key. TODO — list any extra small queries you wrote to answer specific
questions (e.g. average margin of victory in wins), and where they live.

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

TODO — Write each fuzzy concept as an explicit, computable definition. Example:
> **Most improved player** = largest positive change in points-per-game between the
> first half and second half of the season (games 1..k vs k+1..n).

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
