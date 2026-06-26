#!/usr/bin/env python3
"""Compute ground-truth answers for all 10 Phase A questions."""
import csv

# Load data
with open("data/players.csv") as f:
    all_rows = list(csv.DictReader(f))
players = [r for r in all_rows if r["Player"].strip().lower() not in ("team", "tm team", "totals", "opponents") and not r["Number"].strip().startswith("TM") and not r["Player"].strip().upper().startswith("TM ")]

with open("data/games.csv") as f:
    games = list(csv.DictReader(f))

print("=== PHASE A GROUND TRUTH ===\n")

# A1: Games played
print(f"A1 — Games played: {len(games)}")

# A2: Goals leader
players_sorted_g = sorted(players, key=lambda r: int(r["G"]), reverse=True)
print(f"A2 — Goals leader: {players_sorted_g[0]['Player']} with {players_sorted_g[0]['G']} goals")

# A3: Points leader
players_sorted_pts = sorted(players, key=lambda r: int(r["PTS"]), reverse=True)
print(f"A3 — Points leader: {players_sorted_pts[0]['Player']} with {players_sorted_pts[0]['PTS']} points")

# A4: Win-loss record
wins = sum(1 for g in games if g["WL"] == "W")
losses = sum(1 for g in games if g["WL"] == "L")
print(f"A4 — Record: {wins}-{losses}")

# A5: Players with >= 1 goal
scorers = [r for r in players if int(r["G"]) >= 1]
print(f"A5 — Players with ≥1 goal: {len(scorers)}")
for s in scorers:
    print(f"     {s['Player']}: {s['G']} G")

# A6: Avg goals scored per game
avg_su = sum(int(g["SU_Score"]) for g in games) / len(games)
print(f"A6 — Avg SU goals/game: {avg_su:.2f}")

# A7: Avg margin of victory in wins
wins_list = [g for g in games if g["WL"] == "W"]
avg_mov = sum(int(g["SU_Score"]) - int(g["Opp_Score"]) for g in wins_list) / len(wins_list)
print(f"A7 — Avg margin of victory (wins only): {avg_mov:.2f}")
for g in wins_list:
    margin = int(g["SU_Score"]) - int(g["Opp_Score"])
    print(f"     {g['Date']} {g['Opponent']}: {g['SU_Score']}-{g['Opp_Score']} (margin {margin})")

# A8: Highest combined-score game
games_combined = [(int(g["SU_Score"]) + int(g["Opp_Score"]), g) for g in games]
games_combined.sort(key=lambda x: x[0], reverse=True)
top = games_combined[0]
print(f"A8 — Highest combined-score game: {top[1]['Date']} vs {top[1]['Opponent']}, "
      f"{top[1]['SU_Score']}-{top[1]['Opp_Score']} = {top[0]} total")

# A9: Median GP
gp_vals = sorted([int(r["GP"]) for r in players])
n = len(gp_vals)
if n % 2 == 0:
    median_gp = (gp_vals[n//2 - 1] + gp_vals[n//2]) / 2
else:
    median_gp = gp_vals[n//2]
print(f"A9 — Median GP: {median_gp} (n={n} players, sorted GPs: {gp_vals})")

# A10: Best shooting % among players with >= 20 shots
qualified = [r for r in players if int(r["SH"]) >= 20]
for r in qualified:
    r["shoot_pct"] = int(r["G"]) / int(r["SH"])
qualified.sort(key=lambda r: r["shoot_pct"], reverse=True)
print(f"A10 — Best shooting % (≥20 SH):")
for r in qualified:
    print(f"     {r['Player']}: {int(r['G'])}/{int(r['SH'])} = {r['shoot_pct']:.3f}")
print(f"     Winner: {qualified[0]['Player']} at {qualified[0]['shoot_pct']:.3f}")
