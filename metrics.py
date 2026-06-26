#!/usr/bin/env python3
"""
metrics.py — Compute Game Changer, Offense-vs-Defense Lever, and
             One Player to Develop from Syracuse Women's Lacrosse data.

Reads:  data/players.csv   (cumulative player stats)
        data/games.csv     (per-game results)

Prints all results to the console. Does not modify any files.
"""

import csv
import sys
import os
import math

# ──────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ──────────────────────────────────────────────────────────────────────

PLAYERS_PATH = "data/players.csv"
GAMES_PATH   = "data/games.csv"

for path in (PLAYERS_PATH, GAMES_PATH):
    if not os.path.exists(path):
        print(f"ERROR: {path} not found. Cannot proceed without real data.")
        sys.exit(1)

# --- Load players ---
players = []
skipped_rows = []
with open(PLAYERS_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["Player"].strip()
        # Skip non-player rows: Team, Totals, Opponents, or blank names
        if name.lower() in ("team", "totals", "opponents", "tm team", "") \
           or name.upper().startswith("TM "):
            skipped_rows.append(name)
            continue
        # Parse numeric fields; treat blank/missing as 0
        def safe_int(key):
            val = row.get(key, "").strip()
            return int(val) if val else 0
        players.append({
            "number": row["Number"].strip(),
            "name":   name,
            "gp":     safe_int("GP"),
            "g":      safe_int("G"),
            "a":      safe_int("A"),
            "pts":    safe_int("PTS"),
            "sh":     safe_int("SH"),
            "gw":     safe_int("GW"),
            "gb":     safe_int("GB"),
            "dc":     safe_int("DC"),
            "to":     safe_int("TO"),
            "ct":     safe_int("CT"),
            "fouls":  safe_int("FOULS"),
        })

# --- Load games ---
games = []
with open(GAMES_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        games.append({
            "date":      row["Date"].strip(),
            "opponent":  row["Opponent"].strip(),
            "wl":        row["WL"].strip().upper(),
            "su_score":  int(row["SU_Score"]),
            "opp_score": int(row["Opp_Score"]),
        })

total_games = len(games)

print("=" * 72)
print("SYRACUSE WOMEN'S LACROSSE — METRICS REPORT")
print(f"Players loaded: {len(players)}   Games loaded: {total_games}")
if skipped_rows:
    print(f"Skipped non-player rows: {skipped_rows}")
print("=" * 72)


# ──────────────────────────────────────────────────────────────────────
# 2. GAME CHANGER TABLE
# ──────────────────────────────────────────────────────────────────────

# Qualifying threshold: GP >= floor(total_games / 2)
gp_threshold = total_games // 2
qualifying = [p for p in players if p["gp"] >= gp_threshold]

print(f"\n{'─'*72}")
print(f"GAME CHANGER INDEX  (GP threshold ≥ {gp_threshold})")
print(f"{'─'*72}")
print(f"Qualifying players: {len(qualifying)} of {len(players)}\n")

# Compute per-game rates
for p in qualifying:
    gp = p["gp"]
    p["offense_rate"]    = p["pts"]  / gp          # Pts/GP
    p["possession_rate"] = p["dc"]   / gp          # DC/GP
    p["disruption_rate"] = (p["gb"] + p["ct"]) / gp  # (GB+CT)/GP


def mean_std(values):
    """Return (mean, std-dev) for a list of floats."""
    n = len(values)
    mu = sum(values) / n
    var = sum((x - mu) ** 2 for x in values) / n   # population σ
    return mu, math.sqrt(var)


def z_score(x, mu, sigma):
    """Z-score; returns 0.0 if sigma is 0 to avoid division-by-zero."""
    return (x - mu) / sigma if sigma else 0.0


# Compute z-scores across qualifying players
off_vals  = [p["offense_rate"]    for p in qualifying]
pos_vals  = [p["possession_rate"] for p in qualifying]
dis_vals  = [p["disruption_rate"] for p in qualifying]

off_mu, off_sd  = mean_std(off_vals)
pos_mu, pos_sd  = mean_std(pos_vals)
dis_mu, dis_sd  = mean_std(dis_vals)

for p in qualifying:
    p["z_off"] = z_score(p["offense_rate"],    off_mu, off_sd)
    p["z_pos"] = z_score(p["possession_rate"], pos_mu, pos_sd)
    p["z_dis"] = z_score(p["disruption_rate"], dis_mu, dis_sd)
    # Equal weighting (explicit design choice)
    p["game_changer"] = (p["z_off"] + p["z_pos"] + p["z_dis"]) / 3

# Sort descending by GameChanger score
qualifying.sort(key=lambda p: p["game_changer"], reverse=True)

# Print table
header = (f"{'#':<4s} {'Player':<22s} {'GP':>3s}  "
          f"{'Off':>5s} {'Poss':>5s} {'Disr':>5s}  "
          f"{'zOff':>6s} {'zPos':>6s} {'zDis':>6s}  {'GC':>6s}")
print(header)
print("─" * len(header))
for p in qualifying:
    print(f"{p['number']:<4s} {p['name']:<22s} {p['gp']:3d}  "
          f"{p['offense_rate']:5.2f} {p['possession_rate']:5.2f} {p['disruption_rate']:5.2f}  "
          f"{p['z_off']:6.2f} {p['z_pos']:6.2f} {p['z_dis']:6.2f}  "
          f"{p['game_changer']:6.3f}")


# ──────────────────────────────────────────────────────────────────────
# 3. OFFENSE vs DEFENSE LEVER
# ──────────────────────────────────────────────────────────────────────

print(f"\n{'─'*72}")
print("OFFENSE vs DEFENSE LEVER")
print(f"{'─'*72}")

# Season baselines
avg_for     = sum(g["su_score"]  for g in games) / total_games
avg_against = sum(g["opp_score"] for g in games) / total_games

print(f"Season avgFor    = {avg_for:.2f}")
print(f"Season avgAgainst = {avg_against:.2f}")

# Close losses: lost by 1 or 2 goals
close_losses = [g for g in games
                if g["wl"] == "L" and 1 <= (g["opp_score"] - g["su_score"]) <= 2]

print(f"\nClose losses (lost by 1–2 goals): {len(close_losses)}")
for g in close_losses:
    margin = g["opp_score"] - g["su_score"]
    print(f"  {g['date']:10s} {g['opponent']:<25s}  {g['su_score']:2d}-{g['opp_score']:2d}  (margin {margin})")

if close_losses:
    cl_avg_for     = sum(g["su_score"]  for g in close_losses) / len(close_losses)
    cl_avg_against = sum(g["opp_score"] for g in close_losses) / len(close_losses)

    print(f"\nClose-loss avgFor     = {cl_avg_for:.2f}")
    print(f"Close-loss avgAgainst = {cl_avg_against:.2f}")

    # Shortfalls (positive = worse than season baseline)
    offense_shortfall = avg_for - cl_avg_for
    defense_shortfall = cl_avg_against - avg_against

    print(f"\nOffense shortfall  (avgFor − CL_avgFor)        = {offense_shortfall:+.2f}")
    print(f"Defense shortfall  (CL_avgAgainst − avgAgainst) = {defense_shortfall:+.2f}")

    if offense_shortfall > defense_shortfall:
        lever = "offense"
        print(f"\n>>> LEVER = OFFENSE  (scoring shortfall is larger)")
    else:
        lever = "defense"
        print(f"\n>>> LEVER = DEFENSE / POSSESSION  (conceding shortfall is larger)")
else:
    print("\nNo close losses found — lever analysis not applicable.")
    lever = None


# ──────────────────────────────────────────────────────────────────────
# 4. ONE PLAYER TO DEVELOP
# ──────────────────────────────────────────────────────────────────────

print(f"\n{'─'*72}")
print("ONE PLAYER TO DEVELOP")
print(f"{'─'*72}")

if lever and qualifying:
    if lever == "offense":
        # Among top Game Changer players (top half), find one with:
        #   - shots/game in top quartile of full qualifying roster
        #   - shooting % (G/SH) below roster median
        
        # Compute shots/game and shooting % for all qualifying players
        for p in qualifying:
            p["shots_per_game"] = p["sh"] / p["gp"] if p["gp"] else 0
            p["shoot_pct"] = p["g"] / p["sh"] if p["sh"] else 0.0

        # Shots/game: top quartile threshold (75th percentile)
        spg_sorted = sorted([p["shots_per_game"] for p in qualifying])
        q75_idx = int(len(spg_sorted) * 0.75)
        spg_top_quartile_threshold = spg_sorted[q75_idx]

        # Shooting %: median
        sp_sorted = sorted([p["shoot_pct"] for p in qualifying])
        mid = len(sp_sorted) // 2
        if len(sp_sorted) % 2 == 0:
            shoot_median = (sp_sorted[mid - 1] + sp_sorted[mid]) / 2
        else:
            shoot_median = sp_sorted[mid]

        print(f"Lever is OFFENSE")
        print(f"Shots/game top-quartile threshold (≥): {spg_top_quartile_threshold:.2f}")
        print(f"Shooting % (G/SH) roster median:       {shoot_median:.3f}")

        # Top half of qualifying by GameChanger
        top_half = qualifying[:len(qualifying) // 2]
        print(f"Top GameChanger half ({len(top_half)} players):")
        for p in top_half:
            flag_spg = "✓" if p["shots_per_game"] >= spg_top_quartile_threshold else " "
            flag_pct = "✓" if p["shoot_pct"] < shoot_median else " "
            print(f"  {p['name']:<22s}  SH/GP={p['shots_per_game']:.2f} [{flag_spg}top-Q]  "
                  f"G/SH={p['shoot_pct']:.3f} [{flag_pct}<med]  GC={p['game_changer']:.3f}")

        # Find candidates: high volume, low conversion, in top GC half
        candidates = [p for p in top_half
                      if p["shots_per_game"] >= spg_top_quartile_threshold
                      and p["shoot_pct"] < shoot_median]

        if candidates:
            pick = candidates[0]  # highest GameChanger among matches
        else:
            # Fallback: top-GC player with lowest shooting %
            print("\n  No player meets both criteria — falling back to lowest shoot % in top GC half.")
            top_half_with_shots = [p for p in top_half if p["sh"] > 0]
            if top_half_with_shots:
                pick = min(top_half_with_shots, key=lambda p: p["shoot_pct"])
            else:
                pick = top_half[0]

        print(f"\n★  RECOMMENDED: #{pick['number']} {pick['name']}")
        print(f"   GameChanger score:  {pick['game_changer']:.3f}")
        print(f"   Shots/game:         {pick['shots_per_game']:.2f}  (top-quartile ≥ {spg_top_quartile_threshold:.2f})")
        print(f"   Shooting %:         {pick['shoot_pct']:.3f}  (roster median = {shoot_median:.3f})")
        print(f"   Rationale: High shot volume but below-median conversion —")
        print(f"   improving her finishing directly addresses the offense lever.")

    else:  # defense / possession
        # Pick leader in DC/GP or CT/GP
        dc_leader = max(qualifying, key=lambda p: p["possession_rate"])
        ct_leader = max(qualifying, key=lambda p: p["ct"] / p["gp"] if p["gp"] else 0)

        print(f"Lever is DEFENSE / POSSESSION")
        print(f"\nDraw-control leader (DC/GP):")
        print(f"  #{dc_leader['number']} {dc_leader['name']}  DC/GP = {dc_leader['possession_rate']:.2f}")
        print(f"\nCaused-turnover leader (CT/GP):")
        ct_rate = ct_leader["ct"] / ct_leader["gp"]
        print(f"  #{ct_leader['number']} {ct_leader['name']}  CT/GP = {ct_rate:.2f}")

        # Pick whichever has the higher z-score in their domain
        pick = dc_leader  # default to possession
        print(f"\n★  RECOMMENDED: #{pick['number']} {pick['name']}")
        print(f"   Rationale: Leads qualifying players in draw controls per game,")
        print(f"   directly addressing the possession lever.")
else:
    print("Lever analysis was not applicable — no recommendation.")


print(f"\n{'='*72}")
print("Done.")
