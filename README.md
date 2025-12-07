# 🏀 Game Theory Tournament Competition
*A probabilistic March-Madness–style bracket competition for the class*

This project simulates a 64-team single-elimination tournament.  
Each student submits **5 brackets**, and we run many simulated tournaments (e.g., 1,000,000).  

Each team receives a strength value `vᵢ ∈ (0,1)` drawn from a probability distribution.  
Game outcomes are probabilistic:

```
P(i beats j) = vᵢ / (vᵢ + vⱼ)
```

Each bracket earns weighted points for correct predictions.  
For each simulated tournament, the **top-scoring bracket(s)** split **1 point** evenly.  
Students are scored by the total number of points accumulated across all tournaments.

---

## 📁 Files Included

### `tournament_competition.py`
Contains all logic for:
- sampling team strengths  
- tournament simulation  
- correct 64-team bracket seeding  
- bracket validation  
- weighted scoring  
- tie-splitting scoring  
- tournament viewer output  
- leaderboard aggregation  

### `brackets_test.csv`
A test CSV containing 3 example brackets from 3 students.

---

## 📊 Tournament Seeding Structure

This uses **standard 64-team seeding**, ensuring that:
- Seed 1 plays Seed 64 in Round 1  
- Seed 1 plays the winner of (32 vs 33) in Round 2  
- Seed 1 and Seed 2 are in opposite halves and can only meet in the **championship**  

The bracket is generated recursively so that seed positions match real tournament layouts.

Example of initial matchups:
- Game 1: 1 vs 64  
- Game 2: 32 vs 33  
- Game 3: 16 vs 49  
- Game 4: 17 vs 48  
- Game 5: 8 vs 57  
- Game 6: 25 vs 40  
- … through 32 first-round games

The script derives all later rounds automatically from these positions.

---

## 🎲 Team Strength Distributions

Each team receives a random strength value based on seed tier:

- **Seeds 1–16:** stable strong teams (low-variance Beta distributions)  
- **Seeds 17–32:** volatile mid-seeds (higher-variance Beta distributions)  
- **Seeds 33–64:** bimodal “boom or bust” teams (mixtures of two Betas)

This creates realistic upset patterns.

---

## ⚔️ Game Outcome Rule

Games are probabilistic, not deterministic:

```
P(i wins) = vᵢ / (vᵢ + vⱼ)
```

Stronger teams win more often, but upsets are always possible.

---

## 🧮 Scoring System (per bracket, per tournament)

Points for each correct prediction:

| Round         | Games | Points |
|---------------|--------|--------|
| Round of 64   | 32     | 1      |
| Round of 32   | 16     | 2      |
| Sweet 16      | 8      | 4      |
| Elite Eight   | 4      | 8      |
| Final Four    | 2      | 16     |
| Championship  | 1      | 32     |

Example:  
Correctly picking 5 Sweet-16 games earns `5 × 4 = 20` points.

---

## 🏆 Tournament-Level Point Splitting (Important!)

For each simulated tournament:

1. Compute bracket scores.
2. Let `S*` be t*
