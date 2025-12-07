# 🏀 Game Theory Tournament Competition
*A probabilistic March-Madness–style bracket competition for the class*

This project simulates a 64-team single-elimination tournament.  
Each student submits **5 brackets**, and we run many simulated tournaments (e.g., 1,000,000).  

Each team receives a strength value `vᵢ ∈ (0,1)` drawn from a probability distribution.  
Game outcomes are probabilistic:

![probability rule](https://latex.codecogs.com/png.latex?P%28i%20%5Ctext%7Bwins%7D%20%7C%20i%2Cj%29%20%3D%20%5Cfrac%7Bv_i%7D%7Bv_i%20%2B%20v_j%7D)

Each bracket earns weighted points depending on the round.  
For each simulated tournament, the **top-scoring bracket(s)** split **1 point** evenly.  
Students are scored by the total number of points accumulated across all tournaments.

---

## 📁 Files Included

### `tournament_competition.py`
Contains all logic for:
- team strength generation  
- correct 64-team bracket seeding  
- tournament simulation  
- scoring and tie-splitting  
- bracket validation  
- leaderboard calculation  
- text-based bracket viewer  

### `brackets_test.csv`
A small example dataset with 3 valid brackets.

---

## 🎯 Tournament Seeding Structure

We use **standard 64-team seeded bracket construction**, ensuring:

- Seed 1 plays Seed 64 in Round 1  
- Seed 1 plays the winner of Seeds 32 vs 33 in Round 2  
- Seed 1 and Seed 2 only meet in the **championship**

The bracket is built recursively using a standard seed-placement algorithm.

Example initial matchups:

- Game 1: 1 vs 64  
- Game 2: 32 vs 33  
- Game 3: 16 vs 49  
- Game 4: 17 vs 48  
- Game 5: 8 vs 57  
- Game 6: 25 vs 40  
- …  

The script automatically determines later rounds by pairing adjacent winners.

---

## 🎲 Team Strength Distributions

Each team receives a random strength value `vᵢ` drawn from a distribution depending on its seed:

- **Seeds 1–16:** strong, low-variance Beta distributions  
- **Seeds 17–32:** medium-variance Beta distributions  
- **Seeds 33–64:** bimodal mixtures of Betas (“boom-or-bust”)  

This creates realistic upset chances and makes tournaments interesting.

---

## ⚔️ Game Outcome Rule

Game outcomes follow:

![probability rule](https://latex.codecogs.com/png.latex?P%28i%20%5Ctext%7Bwins%7D%20%5Cmid%20i%2Cj%29%20%3D%20%5Cfrac%7Bv_i%7D%7Bv_i%20%2B%20v_j%7D)

This gives stronger teams higher win probability while still allowing upsets.

---

## 🧮 Scoring System

Points for each correct prediction:

| Round         | Games | Points |
|---------------|--------|--------|
| Round of 64   | 32     | 1      |
| Round of 32   | 16     | 2      |
| Sweet 16      | 8      | 4      |
| Elite Eight   | 4      | 8      |
| Final Four    | 2      | 16     |
| Championship  | 1      | 32     |

---

## 🏆 Tournament-Level Point Splitting

In each simulated tournament:

1. Compute bracket scores.
2. Let `S*` be the max score.
3. Let `T` be all brackets that achieved `S*`.
4. Each bracket receives:

![tie split](https://latex.codecogs.com/png.latex?\text{PointsPerBracket}%20=%20\frac{1}{|T|})

Examples:

- 1 best bracket → earns **1.0** point  
- 4 tied → each earns **0.25**  
- 10 tied → each earns **0.1**  

---

## 📥 Bracket Submission Format

Students submit a CSV file:

```
student,bracket_name,g1,g2,...,g63
```

Where:

- `student` = name or ID  
- `bracket_name` = label (A, B, C, …)  
- `g1` … `g63` are the predicted winning **seed numbers (1–64)**

The script will reject invalid brackets (wrong structure or impossible predictions).

Game order:

- Round of 64 → `g1`–`g32`  
- Round of 32 → `g33`–`g48`  
- Sweet 16 → `g49`–`g56`  
- Elite Eight → `g57`–`g60`  
- Final Four → `g61`–`g62`  
- Championship → `g63`  

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

- A detailed text printout comparing a sample bracket against a simulated tournament  
- Bracket point totals with fractional tie-splitting  
- Student leaderboard  

To adjust number of simulations:

```python
NUM_TOURNAMENTS = 10**6
```
