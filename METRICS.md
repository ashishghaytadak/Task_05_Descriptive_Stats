# Metric Definitions — Task 05

These definitions are written so that a human reader **or** a language model can
apply each metric unambiguously to the Syracuse Women's Lacrosse 2026 cumulative
statistics.

---

## 1. Most Improved Player

**Definition.** For each player, split the season into two halves by game number
(games 1 … k and k+1 … n, where k = ⌊n/2⌋). Compute points-per-game (PPG) in
each half. The *most improved player* is the one with the **largest positive
change** in PPG from the first half to the second half:

> Δ PPG = PPG_second_half − PPG_first_half

The player with the highest positive Δ PPG is the most improved.

> [!IMPORTANT]
> **This metric is NOT computable from the cumulative-stats CSV.**
> The cumulative PDF provides only season totals (GP, G, A, PTS, …) per player,
> not per-game box scores. To compute first-half vs. second-half PPG we would
> need a row per player per game. If per-game box-score data is added to
> `data/` later, this metric can be calculated. Until then, it remains a
> definitional placeholder.

---

## 2. Game Changer (composite z-score index)

**Qualifying population.** Only players with GP ≥ ⌊(team's total games) / 2⌋
are eligible. This filters out low-sample-size players whose per-game rates
would be unreliable.

**Three per-game rates.** For each qualifying player compute:

| Rate | Formula | Captures |
|------|---------|----------|
| Offense | Pts / GP | Scoring contribution |
| Possession | DC / GP | Draw-control impact |
| Disruption | (GB + CT) / GP | Ball recovery & caused turnovers |

**Z-score standardisation.** Convert each rate to a z-score across the
qualifying population:

> z = (x − μ) / σ

where μ and σ are the mean and standard deviation of that rate among qualifying
players.

**Composite score.**

> GameChanger = (z_offense + z_possession + z_disruption) / 3

The three pillars are **weighted equally** — this is an explicit design choice.
An alternative weighting (e.g., double-weighting offense) could be justified but
is not used here. Players are ranked by GameChanger descending; higher is
better.

---

## 3. Offense vs. Defense Lever

This metric identifies **which side of the ball** cost the team its closest
losses, pointing to the highest-impact area for improvement.

**Season baselines.**

> avgFor = mean of SU_Score across all games
> avgAgainst = mean of Opp_Score across all games

**Close losses.** A game is a *close loss* if WL = L **and** the margin is
1 or 2 goals:

> Opp_Score − SU_Score ∈ {1, 2}

**Close-loss averages.**

> closeLoss_avgFor = mean SU_Score in close losses only
> closeLoss_avgAgainst = mean Opp_Score in close losses only

**Shortfalls.**

> offense_shortfall = avgFor − closeLoss_avgFor
> defense_shortfall = closeLoss_avgAgainst − avgAgainst

(Both are positive when the close-loss performance is worse than the season
baseline.)

**Decision rule.**

- If offense_shortfall > defense_shortfall → the lever is **offense** (the team
  scored further below its average than the opponent exceeded theirs).
- Otherwise → the lever is **defense/possession**.

---

## 4. One Player to Develop

Given the lever identified above, this metric names a single player whose
profile suggests the highest marginal return from targeted development.

### If the lever is **offense**:

1. Take the top Game Changer players (e.g., top half of qualifying players by
   GameChanger score).
2. Among them, find the player whose **shots per game** (SH / GP) is in the
   **top quartile** of the full qualifying roster, but whose **shooting
   percentage** (G / SH) is **below the roster median** (calculate this median only across qualifying players who have taken at least one shot, `SH > 0`).

   This targets a player who *gets enough shots* (volume is already there) but
   *converts at a below-average rate* — the classic "if she just finished
   better" candidate.

3. If no player meets both criteria, relax to the top-GameChanger player with
   the lowest shooting percentage.

### If the lever is **defense / possession**:

Pick the qualifying player who leads in **DC / GP** (draw-control rate) or
**CT / GP** (caused-turnover rate) — whichever defensive rate is more relevant
to the lever. Developing this player's possession or disruption skill directly
addresses the identified weakness.

---

*These definitions are intentionally mechanical so that results are
reproducible. Any analyst (or LLM) given the same CSV inputs should arrive at
identical answers.*
