# Prompt & Response Log — Task 05

Record every exchange as you go. Reconstructing this at the end never works.
For each entry fill in: model + version, the **exact** prompt, the response
(trim long ones but keep the part that contains the answer), your ground-truth
value, and a verdict.

**Models tested in this log:**
- Model 1: TODO (e.g. Claude Opus 4.x) — how data was supplied: TODO
- Model 2 (optional, bonus): TODO

Verdict key: ✅ correct · ⚠️ partially correct / right number wrong reasoning ·
❌ wrong · 🧮 answered by writing/running code · 💬 answered conversationally

---

## Phase A — factual questions

### A1 — Games played
- **Model / version:**
- **Prompt:**
- **Response:**
- **Ground truth (from games.csv):**
- **Verdict:**
- **Notes (did it compute or restate? confident?):**

### A2 — Goals leader
- **Model / version:**
- **Prompt:**
- **Response:**
- **Ground truth (players.csv, max G):**
- **Verdict:**
- **Notes:**

### A3 — Points leader
- **Prompt:**
- **Response:**
- **Ground truth (players.csv, max Pts):**
- **Verdict:**
- **Notes:**

### A4 — Win–loss record
- **Prompt:**
- **Response:**
- **Ground truth (games.csv, W vs L):**
- **Verdict:**
- **Notes:**

### A5 — Players with ≥1 goal
- **Prompt:**
- **Response:**
- **Ground truth (count G > 0):**
- **Verdict:**
- **Notes:**

### A6 — Average goals scored per game
- **Prompt:**
- **Response:**
- **Ground truth (mean SU score):**
- **Verdict:**
- **Notes:**

### A7 — Average margin of victory in wins
- **Prompt:**
- **Response:**
- **Ground truth (mean (SU − opp) where W):**
- **Verdict:**
- **Notes:**

### A8 — Highest combined-score game
- **Prompt:**
- **Response:**
- **Ground truth (max SU + opp):**
- **Verdict:**
- **Notes:**

### A9 — Median GP across roster
- **Prompt:**
- **Response:**
- **Ground truth (median GP):**
- **Verdict:**
- **Notes:**

### A10 — Best shooting % (≥20 shots)
- **Prompt:**
- **Response:**
- **Ground truth (max G/Sh, filtered Sh ≥ 20):**
- **Verdict:**
- **Notes:**

---

## Phase B — judgment questions
(Add entries as you go. Record the metric definition you gave the model, each
prompt-engineering iteration, and how you validated the final answer.)

### B1 — Metric definition supplied
- **Concept being operationalized:**
- **Definition given to the model:**
- **Prompt:**
- **Response:**
- **Did it apply your definition faithfully or drift to its own?**
- **Your independent recomputation:**
- **Verdict:**

### B2 — The advisory "coach" question
- **Prompt (final version after iteration):**
- **Earlier iterations that failed and why:**
- **Response:**
- **Validation — did the recommendation follow from the numbers?**
- **Verdict:**
