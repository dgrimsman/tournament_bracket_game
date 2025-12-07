🏀 Game Theory Tournament Competition

A probabilistic March-Madness–style bracket competition

This project simulates a 64-team single-elimination tournament.
Each student submits 5 brackets, and we run many simulated tournaments (typically 1,000,000).

Each team receives a strength value vᵢ ∈ (0,1) drawn from a probability distribution.
Game outcomes are probabilistic:

P(i beats j) = vᵢ / (vᵢ + vⱼ)


Brackets earn points for correctly predicting winners; deeper rounds are worth more.
For each simulated tournament, the best-scoring bracket(s) split 1 point equally.
A student's total score is the sum of points across all their brackets.

📁 Files Included
tournament_competition.py

Main Python script containing:

Team strength distributions

Tournament simulation

Proper 64-team bracket seeding

Weighted scoring system

Tie-splitting score allocation

Bracket validation

Tournament viewer (text-based)

Leaderboard calculation

brackets_test.csv

A small set of example brackets from three students, valid under proper seeding.

📊 Tournament Seeding Structure

This project uses standard 64-team tournament seeding, ensuring:

Seed 1 never plays Seed 2 until the championship

Seed 1 plays Seed 64 in Round 1

Seed 1 meets the winner of (32 vs 33) in Round 2

Seeds are placed symmetrically on opposite sides of the bracket

The structure matches the logic used in real-world tournaments

The initial Round-of-64 matchups are determined recursively via:

seed_order(64) → [1, 64, 32, 33, 16, 49, 17, 48, 8, 57, 25, 40, ...]


This list defines the ordering of teams in Round 1.

🎲 Team Strength Distributions

Each team receives a random strength value vᵢ drawn independently from:

Seeds 1–16: stable, strong, low-variance Beta distributions

Seeds 17–32: more volatile medium-variance Beta distributions

Seeds 33–64: bimodal Beta mixtures (“boom-or-bust” teams)

This produces realistic upset behavior: some lower seeds occasionally run deep.

⚔️ Game Outcome Model

Games are not deterministic. The probability that team i beats team j is:

P(i wins) = vᵢ / (vᵢ + vⱼ)


This ensures:

Stronger teams win more often

Upsets remain possible

Simulation captures randomness inherent in real tournaments

🧮 Scoring System (per bracket per tournament)

Each correct predicted winner yields:

Round	Games	Points per pick
Round of 64	32	1 point
Round of 32	16	2 points
Sweet 16	8	4 points
Elite Eight	4	8 points
Final Four	2	16 points
Championship	1	32 points

Example:
Correctly predicting 6 games in the Sweet 16 → 6 × 4 = 24 points.

🏆 Tournament-Level Scoring (Tie-Splitting)

For each simulated tournament:

Compute all bracket scores.

Let S* be the highest score.

Let T be all brackets with score S*.

Each bracket in T receives:

1 / |T| points


Examples:

A single best bracket → earns 1.0 point

4 tied best brackets → each earns 0.25 points

10 tied → each earns 0.1 points

A student’s final total is the sum over all tournaments and all brackets they submitted.

📥 Bracket Submission Format

Students submit a CSV file named, e.g., brackets.csv with the format:

student,bracket_name,g1,g2,...,g63


Where:

student = name or ID

bracket_name = label such as A, B, C, ...

g1–g63 = predicted winner seed numbers 1–64

The script checks consistency:

winners must be valid seeds

predictions must match allowable teams in each game based on the bracket structure

exactly 63 entries are required

📝 Example Submission (brackets_test.csv)

This example is included with the code:

student,bracket_name,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15,g16,g17,g18,g19,g20,g21,g22,g23,g24,g25,g26,g27,g28,g29,g30,g31,g32,g33,g34,g35,g36,g37,g38,g39,g40,g41,g42,g43,g44,g45,g46,g47,g48,g49,g50,g51,g52,g53,g54,g55,g56,g57,g58,g59,g60,g61,g62,g63
alice,A,1,32,16,17,8,25,9,24,4,29,13,20,5,28,12,21,2,31,15,18,7,26,10,23,3,30,14,19,6,27,11,22,1,16,8,9,4,13,5,12,2,15,7,10,3,14,6,11,1,8,4,5,2,7,3,6,1,4,2,3,1,2,1
bob,A,64,33,49,48,57,40,56,24,61,36,52,45,60,37,53,44,63,34,50,47,58,39,55,42,62,35,51,46,59,38,54,43,64,49,57,56,61,52,60,53,63,50,58,55,62,51,59,54,64,57,61,60,63,58,62,59,64,61,63,62,64,63,64
charlie,A,64,33,49,48,57,25,56,41,4,55,52,20,5,51,53,21,63,47,50,45,7,26,23,42,3,39,14,37,6,30,11,43,64,16,8,56,36,12,37,21,63,50,39,55,3,46,6,11,1,8,52,12,63,21,3,59,1,9,17,25,1,17,1


Each row contains:

32 Round-of-64 predictions (g1–g32)

16 Round-of-32 predictions (g33–g48)

8 Sweet-16 predictions (g49–g56)

4 Elite-8 predictions (g57–g60)

2 Final-Four predictions (g61, g62)

1 Championship prediction (g63)

🔍 Running the Simulation
1. Install Python 3.9+
2. Prepare a bracket file (brackets.csv or brackets_test.csv)
3. Run the script
python tournament_competition.py


You will see:

A detailed game-by-game printout comparing one bracket against a simulated tournament

Total points over many simulations

Student leaderboard

Change the number of simulations:

Inside the script:

NUM_TOURNAMENTS = 10**6

🧾 Example Output (shortened)
=== Tournament vs Bracket: alice [A] ===

--- Round 1 (weight 1 per correct pick) ---
G 1: Seed 1 (v=0.812) vs Seed 64 (v=0.203) → actual: 1, predicted: 1 [✓]
G 2: Seed 32 (v=0.455) vs Seed 33 (v=0.610) → actual: 33, predicted: 32 [✗]
...

Round 1 points: 22
...

TOTAL POINTS for alice [A]: 87
