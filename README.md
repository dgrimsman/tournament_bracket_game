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
2. Let `S*` be the max score.
3. Let `T` be all brackets tied for best.
4. Each bracket in `T` receives:

```
1 / |T| points
```

Examples:
- 1 best bracket → it gets **1.0** point  
- 4 tied brackets → each gets **0.25**  
- 10 tied brackets → each gets **0.1**  

A student's final score is the sum over all tournaments and all brackets they submitted.

---

## 📥 Bracket Submission Format

Students submit their 5 brackets in a CSV:

```
student,bracket_name,g1,g2,...,g63
```

Where each `g#` is the predicted **seed number (1–64)** winning that game.

- Round of 64 → g1 to g32  
- Round of 32 → g33 to g48  
- Sweet 16 → g49 to g56  
- Elite Eight → g57 to g60  
- Final Four → g61 to g62  
- Championship → g63  

The script validates that each bracket follows the true tournament structure.

---

## 📝 Example Bracket File (`brackets_test.csv`)

```
student,bracket_name,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15,g16,g17,g18,g19,g20,g21,g22,g23,g24,g25,g26,g27,g28,g29,g30,g31,g32,g33,g34,g35,g36,g37,g38,g39,g40,g41,g42,g43,g44,g45,g46,g47,g48,g49,g50,g51,g52,g53,g54,g55,g56,g57,g58,g59,g60,g61,g62,g63
alice,A,1,32,16,17,8,25,9,24,4,29,13,20,5,28,12,21,2,31,15,18,7,26,10,23,3,30,14,19,6,27,11,22,1,16,8,9,4,13,5,12,2,15,7,10,3,14,6,11,1,8,4,5,2,7,3,6,1,4,2,3,1,2,1
bob,A,64,33,49,48,57,40,56,24,61,36,52,45,60,37,53,44,63,34,50,47,58,39,55,42,62,35,51,46,59,38,54,43,64,49,57,56,61,52,60,53,63,50,58,55,62,51,59,54,64,57,61,60,63,58,62,59,64,61,63,62,64,63,64
charlie,A,64,33,49,48,57,25,56,41,4,55,52,20,5,51,53,21,63,47,50,45,7,26,23,42,3,39,14,37,6,30,11,43,64,16,8,56,36,12,37,21,63,50,39,55,3,46,6,11,1,8,52,12,63,21,3,59,1,9,17,25,1,17,1
```

---

## 🧪 Running the Simulation

Run:

```
python tournament_competition.py
```

You will see:

- A detailed printout comparing one bracket to a simulated tournament  
- Final bracket and student scores (including fractional tie-splits)  

Change the number of simulated tournaments by editing:

```python
NUM_TOURNAMENTS = 10**6
```

---

## 🔧 Instructor-Friendly Features

- Strict bracket validation  
- Probabilistic team strengths & game outcomes  
- Realistic upset behavior  
- Weighted scoring  
- Fair tie-splitting  
- Detailed bracket viewer  
- Simple CSV format for student submissions  

---

## 🚀 Optional Future Extensions

- Add team names / regions  
- Graphical bracket visualization  
- Expected-value analysis for each bracket  
- Web UI for tournament viewing and submissions  

---

If you'd like, I can also generate:

- A **printable bracket template**  
- SVG diagrams explaining seeding  
- A GitHub Pages site for pretty presentation

Just let me know!
