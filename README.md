# Task 05 — Descriptive Statistics and Large Language Models

*From ground truth to LLM judgment.*

This repo documents an experiment: I computed trustworthy descriptive statistics
for a small dataset using my own verified code, then interrogated a large language
model about that same data in natural language and checked every answer against my
ground truth.


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
I tested Claude 4.8 Opus by supplying both `players.csv` and `games.csv` as raw CSV text directly in the prompt. I asked 10 factual questions ranging from simple lookups (e.g., goals leader) to complex filtering and traps (e.g., finding the highest combined score, identifying median GP while handling the "TM Team" row). 

Claude 4.8 Opus performed remarkably well. (Note on the format experiment: I ran the questions with both raw CSV and a formatted markdown table to check if format changed accuracy—it made no difference; the model went 10/10 either way). It avoided the trap of assuming the highest-scoring game was a win, correctly excluded the "TM Team" row when calculating the median GP, and properly filtered players with ≥20 shots before determining the best shooting percentage. See [`prompt_log.md`](prompt_log.md) for the full record.

### Phase B — derived metrics and judgment
I supplied Claude 4.8 Opus with my custom "Game Changer Index" definition and asked it to rank the qualifying players. The test here was the "Lahah drift test": Izzy Lahah is a defensive specialist who scores virtually no goals but dominates in ground balls and caused turnovers. If the model followed my math, she had to rank #2. Claude passed with flying colors—it faithfully applied the formula, successfully computed the z-scores, and placed Lahah exactly at #2, resisting the typical LLM urge to just rank by points.

For the advisory coach question, Claude successfully identified that the team's narrow losses were due to an offensive shortfall (scoring 8.00 vs the 9.65 average)—though it is worth noting this lever rests on a thin margin across only two close losses (n=2).

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

**Successes:**
- **Methodological Trap Avoidance:** Claude easily sidestepped logical traps in the Phase A questions. It correctly identified that the highest combined-score game was a blowout loss. For the median GP, it explicitly stated it was excluding the "TM Team" row (though on this specific dataset, the median GP is 17 whether you include that row or not, so the model's explicit methodology was the real success here).
- **Following Strict Math:** In Phase B, Claude faithfully executed the Game Changer z-score framework. It didn't "drift" back to a standard goals-based ranking, placing defensive specialist Izzy Lahah at #2 precisely as the math dictated.
- **Resolving Ambiguity via Methodological Comparison:** A fascinating finding emerged during the "One Player to Develop" metric, which requires a player to have top-quartile shot volume and below-median finishing. Qualifying is the intersection of two filters (GameChanger top-half and the median). One high-volume shooter (Ashlee Volpe, 30% on 2.35 SH/GP) has below-median finishing but is excluded by the GameChanger gate (#10 out of 18). This leaves Guzik sitting on a knife-edge: if the median shooting percentage includes zero-shot players, the median drops to 36.64% and Guzik (37.29%) fails to qualify. If zero-shot players are excluded, the median is 37.50% and Guzik qualifies. Rather than just guessing, the two interpretations (0-shot included vs excluded) were explicitly computed and compared, and the natural reading (excluding 0-shot) was found to produce the most defensible coaching pick: improving the efficiency of a 5.9-shots/game star. I updated the formal `METRICS.md` definition to codify this natural reading.

**Failures & Limitations:**
- **Zero-Shot Fragility:** While Claude 4.8 Opus went 10/10 on the factual questions with raw CSV data, older or smaller models often stumble on filtering logic (like filtering for ≥20 shots before calculating percentages) without being explicitly asked to run code or think step-by-step.
- **Definitional Ambiguity:** The experiment highlighted that highly capable LLMs can explicitly compare and resolve underspecified ambiguities (like how to handle 0-shot players) in ways a rigid script wouldn't, producing better real-world coaching advice than a naive heuristic.

**Conclusion:** I would trust an LLM like Claude 4.8 Opus to perform initial exploratory data analysis and to translate mechanical insights into strategic advice. However, for generating the ground-truth numbers that drive business or coaching decisions, I would still insist on deterministic Python scripts to guarantee consistency.

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
