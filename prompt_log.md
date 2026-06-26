# Prompt & Response Log — Task 05

Record every exchange as you go. Reconstructing this at the end never works.
For each entry fill in: model + version, the **exact** prompt, the response
(trim long ones but keep the part that contains the answer), your ground-truth
value, and a verdict.

**Models tested in this log:**
- Model 1: Claude 4.8 Opus — how data was supplied: Raw CSV pasted directly into the prompt.
- Model 2 (optional, bonus): None

Verdict key: ✅ correct · ⚠️ partially correct / right number wrong reasoning ·
❌ wrong · 🧮 answered by writing/running code · 💬 answered conversationally

---

## Phase A — factual questions

### A1 — Games played
- **Model / version:** Claude 4.8 Opus
- **Prompt:** How many games did the team play this season?
- **Response:** "Based on the games.csv data provided, the team played 20 games."
- **Ground truth (from games.csv):** 20
- **Verdict:** ✅ correct

### A2 — Goals leader
- **Model / version:** Claude 4.8 Opus
- **Prompt:** Which player led the team in goals, and how many?
- **Response:** "Molly Guzik led the team in goals with 44."
- **Ground truth (players.csv, max G):** Guzik, 44
- **Verdict:** ✅ correct

### A3 — Points leader
- **Prompt:** Which player had the most total points?
- **Response:** "Molly Guzik had the most total points with 54."
- **Ground truth (players.csv, max Pts):** Guzik, 54
- **Verdict:** ✅ correct

### A4 — Win–loss record
- **Prompt:** What was the team's win-loss record?
- **Response:** "The team's win-loss record was 14 wins and 6 losses (14-6)."
- **Ground truth (games.csv, W vs L):** 14-6
- **Verdict:** ✅ correct

### A5 — Players with ≥1 goal
- **Prompt:** How many players scored at least one goal?
- **Response:** "17 players scored at least one goal."
- **Ground truth (count G > 0):** 17
- **Verdict:** ✅ correct

### A6 — Average goals scored per game
- **Prompt:** What was the team's average goals scored per game?
- **Response:** "The team scored 193 goals across 20 games, for an average of 9.65 goals per game."
- **Ground truth (mean SU score):** 9.65
- **Verdict:** ✅ correct

### A7 — Average margin of victory in wins
- **Prompt:** What was the average margin of victory in wins only?
- **Response:** "In the 14 games Syracuse won, the average margin of victory was 3.93 goals."
- **Ground truth (mean (SU − opp) where W):** 3.93
- **Verdict:** ✅ correct

### A8 — Highest combined-score game
- **Prompt:** Which game had the highest combined score?
- **Response:** "The highest combined score was 28 goals, which happened in the game against North Carolina on 4/24/26 (Syracuse scored 9, North Carolina scored 19)."
- **Ground truth (max SU + opp):** vs UNC 4/24, 9–19 = 28
- **Verdict:** ✅ correct
- **Notes:** Avoided the trap of assuming the highest combined score was a win.

### A9 — Median GP across roster
- **Prompt:** What was the median games-played (GP) across the roster?
- **Response:** "The median GP across the roster of 33 players (excluding the TM Team row) is 17."
- **Ground truth (median GP):** 17
- **Verdict:** ✅ correct
- **Notes:** Trap passed. Whether excluding TM Team or not, the answer remains 17, but it correctly noted the 33 actual players.

### A10 — Best shooting % (≥20 shots)
- **Prompt:** Best shooting % among players with ≥20 shots?
- **Response:** "Among players with at least 20 shots, Emma Muchnick had the highest shooting percentage at 44.6% (25 goals on 56 shots)."
- **Ground truth (max G/Sh, filtered Sh ≥ 20):** Muchnick, 25/56 = 44.6%
- **Verdict:** ✅ correct
- **Notes:** Applied the shot filter correctly, avoiding picking Lahah at 100% (1/1).

---

## Phase B — judgment questions

### B1 — Metric definition supplied
- **Concept being operationalized:** Game Changer Index (equal weighting of offense, possession, and disruption z-scores).
- **Definition given to the model:** 
"I want to test your ability to apply a specific analytical framework. Here is my metric definition:
**Game Changer Index:** For players with GP >= 10 (half of 20 games), compute three per-game rates:
- offense = PTS/GP
- possession = DC/GP
- disruption = (GB+CT)/GP
Convert each rate to a z-score across qualifying players, then: GameChanger = (z_offense + z_possession + z_disruption) / 3. The three pillars are equally weighted.
Using this exact definition, compute the Game Changer score for every qualifying player and rank them. Show the per-game rates and z-scores."
- **Response:** Claude 4.8 Opus correctly calculated the scores using a population standard deviation. Top 4: Guzik 1.87, Lahah 0.50, Muchnick 0.26, Trinkaus 0.25.
- **Did it apply your definition faithfully or drift to its own?** Yes, it passed the Lahah drift test flawlessly. Izzy Lahah is a defensive specialist (52 GB, 31 CT, barely scores), yet the model correctly identified her as #2 strictly by applying the math for disruption z-score. It did not drift back into a points-based ranking.
- **Your independent recomputation:** Matches perfectly.
- **Verdict:** ✅ correct. 

### B2 — The advisory "coach" question
- **Prompt:** "As an advisory coach analyzing this data: which ONE player would you prioritize for development, and what specific skill should she work on? Justify your recommendation using only the statistics in the data."
- **Response:** "Based on the Lever analysis, offense is the lever that failed in our tightest situations (scoring 8.00 vs 9.65 avg in the two close losses against Stanford and Navy). To address this, I recommend prioritizing Molly Guzik for development, focusing specifically on her shooting accuracy and finishing. She has an elite volume of shots (5.9/game) which places her in the top quartile, but her shooting percentage is 37.3%, which sits below the roster median of players who shoot (37.5%). Improving the efficiency of our highest-volume shooter yields the highest marginal return in goals, addressing the exact gap we saw in close losses."
- **Validation — did the recommendation follow from the numbers?** Yes. By correctly taking the median shooting percentage only among players who took at least one shot (SH > 0), the median is 37.5%. Guzik's 37.3% falls below this median, making her satisfy both the top-quartile volume constraint AND the below-median finishing constraint. The model arrived exactly at the most defensible coaching pick organically.
- **Verdict:** ✅ correct.
