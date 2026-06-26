# Prompt & Response Log — Task 05

Record every exchange as you go. Reconstructing this at the end never works.
For each entry fill in: model + version, the **exact** prompt, the response
(trim long ones but keep the part that contains the answer), your ground-truth
value, and a verdict.

**Models tested in this log:**
- Model 1: Claude 3.5 Sonnet — how data was supplied: Raw CSV pasted directly into the prompt.
- Model 2 (optional, bonus): None

Verdict key: ✅ correct · ⚠️ partially correct / right number wrong reasoning ·
❌ wrong · 🧮 answered by writing/running code · 💬 answered conversationally

---

## Phase A — factual questions

### A1 — Games played
- **Model / version:** Claude 3.5 Sonnet
- **Prompt:** How many games did the team play this season?
- **Response:** "Based on the games.csv file, Syracuse played 20 games in the 2026 season."
- **Ground truth (from games.csv):** 20
- **Verdict:** ✅ correct
- **Notes:** Confidently answered without writing code.

### A2 — Goals leader
- **Model / version:** Claude 3.5 Sonnet
- **Prompt:** Which player led the team in goals, and how many?
- **Response:** "Molly Guzik led the team with 44 goals."
- **Ground truth (players.csv, max G):** Molly Guzik, 44
- **Verdict:** ✅ correct
- **Notes:** Simple lookup, handled easily.

### A3 — Points leader
- **Prompt:** Which player had the most total points?
- **Response:** "Molly Guzik had the most total points with 54 points (44 goals and 10 assists)."
- **Ground truth (players.csv, max Pts):** Molly Guzik, 54
- **Verdict:** ✅ correct
- **Notes:** Added the breakdown of goals and assists unprompted.

### A4 — Win–loss record
- **Prompt:** What was the team's win-loss record?
- **Response:** "The team's win-loss record was 14 wins and 6 losses (14-6)."
- **Ground truth (games.csv, W vs L):** 14-6
- **Verdict:** ✅ correct
- **Notes:** Counted Ws and Ls correctly from the WL column.

### A5 — Players with ≥1 goal
- **Prompt:** How many players scored at least one goal?
- **Response:** "Looking at the players.csv data, 17 players scored at least one goal." (Lists all 17 names).
- **Ground truth (count G > 0):** 17
- **Verdict:** ✅ correct
- **Notes:** Correctly excluded the goalie and defenders with 0 goals.

### A6 — Average goals scored per game
- **Prompt:** What was the team's average goals scored per game?
- **Response:** "The team scored a total of 193 goals across 20 games, which averages out to 9.65 goals per game."
- **Ground truth (mean SU score):** 9.65
- **Verdict:** ✅ correct
- **Notes:** Computed the sum and mean accurately.

### A7 — Average margin of victory in wins
- **Prompt:** What was the average margin of victory in wins only?
- **Response:** "There were 14 wins. Summing the margins (15-7=8, 13-10=3, 13-3=10, 13-3=10, 9-6=3, 6-5=1, 6-5=1, 10-8=2, 16-7=9, 10-8=2, 10-9=1, 10-9=1, 11-9=2, 8-6=2) gives a total margin of 55 goals. 55 / 14 = 3.93 goals on average."
- **Ground truth (mean (SU − opp) where W):** 3.93
- **Verdict:** ✅ correct
- **Notes:** Showed its work line by line to avoid hallucination.

### A8 — Highest combined-score game
- **Prompt:** Which game had the highest combined score?
- **Response:** "The highest combined score was the game against North Carolina on 4/24/26. Syracuse scored 9 and North Carolina scored 19, for a combined total of 28 goals. (Note: This was a loss for Syracuse)."
- **Ground truth (max SU + opp):** vs North Carolina (4/24), 9–19, combined 28
- **Verdict:** ✅ correct
- **Notes:** Avoided the common LLM trap of assuming the highest-scoring game must be a win.

### A9 — Median GP across roster
- **Prompt:** What was the median games-played (GP) across the roster?
- **Response:** "First, I'll extract the GP for all 33 actual players (excluding the 'TM Team' row)... The median of these 33 values is 17."
- **Ground truth (median GP):** 17
- **Verdict:** ✅ correct
- **Notes:** Successfully recognized that "TM Team" should be excluded and handled the bench players correctly.

### A10 — Best shooting % (≥20 shots)
- **Prompt:** Best shooting % among players with ≥20 shots?
- **Response:** "Filtering for players with SH >= 20, the highest shooting percentage belongs to Emma Muchnick, who scored 25 goals on 56 shots for a shooting percentage of 44.6%."
- **Ground truth (max G/Sh, filtered Sh ≥ 20):** Emma Muchnick, 25/56 = 44.6%
- **Verdict:** ✅ correct
- **Notes:** Avoided the trap of skipping the filter (which would have picked a 1-for-1 player).

---

## Phase B — judgment questions
(Add entries as you go. Record the metric definition you gave the model, each
prompt-engineering iteration, and how you validated the final answer.)

### B1 — Metric definition supplied
- **Concept being operationalized:** Game Changer Index (equal weighting of offense, possession, and disruption z-scores).
- **Definition given to the model:** Provided exact definition from METRICS.md.
- **Prompt:** "Using this exact definition, compute the Game Changer score for every qualifying player and rank them. Show the per-game rates and z-scores."
- **Response:** Claude returned a table with 18 qualifying players. The top 3 were: 1. Molly Guzik (GC = 1.87), 2. Izzy Lahah (GC = 0.50), 3. Emma Muchnick (GC = 0.26).
- **Did it apply your definition faithfully or drift to its own?** Yes, it applied the definition faithfully. It correctly placed defensive specialist Izzy Lahah (1 goal all season) at #2 entirely based on her extreme disruption z-score (52 GB, 57 CT). It did not drift back to a goals/points ranking.
- **Your independent recomputation:** Guzik 1.866, Lahah 0.496, Muchnick 0.261
- **Verdict:** ✅ correct. Claude executed the multi-step mathematical framework flawlessly.

### B2 — The advisory "coach" question
- **Prompt (final version after iteration):** "As an advisory coach analyzing this data: which ONE player would you prioritize for development, and what specific skill should she work on? Justify your recommendation using only the statistics in the data."
- **Earlier iterations that failed and why:** None needed, asked directly after B1.
- **Response:** "Based on the data, the team suffered two close losses (Stanford 6-8, Navy 10-11). In these games, the offense scored significantly below its season average (8.00 vs 9.65), pointing to offense as the primary lever for improvement. To address this, I would prioritize developing Molly Guzik's shooting accuracy. She is already taking a massive 5.9 shots per game (118 total) but converting at only 37.3%, which is below the team's top finishers like Muchnick (44.6%). Improving the efficiency of your highest-volume shooter will yield the largest marginal increase in goals."
- **Validation — did the recommendation follow from the numbers?** Yes, and this was an incredible result. My mechanical python script failed to find a player who strictly fit the rigid rule (top-quartile volume AND below-median finishing), but Claude naturally identified the *spirit* of the rule. It pointed out that Guzik has elite volume but trails the top finishers in efficiency, making her the highest-leverage development candidate.
- **Verdict:** ✅ correct (and arguably better coaching advice than the strict Python heuristic).
