🏀 Game Theory Tournament Competition

A probabilistic March-Madness-style bracket competition for the class

This project simulates a 64-team single-elimination tournament.
Each student submits 5 brackets, and we run many simulated tournaments (e.g. 1,000,000).

Each simulated tournament assigns a value to each team from a known probability distribution.
Game outcomes are probabilistic:

P(i beats j)=vivi+vj.
P(i beats j)=
v
i
	​

+v
j
	​

v
i
	​

	​

.

Brackets earn points for correctly predicting winners in each round.
For each simulated tournament, the best-scoring bracket(s) split 1 point equally.
Students are ranked by total points accumulated across all tournaments.

📁 Files in This Repository

tournament_competition.py
Main Python script for:

reading brackets

validating bracket structure

generating team strengths

simulating tournaments

computing weighted bracket scores

splitting points among tied best brackets

aggregating student scores

printing bracket-vs-simulation comparisons

brackets_test.csv
Example file with 3 sample brackets (one per student), all valid under standard seeding.

📊 Tournament Structure

The tournament uses standard 64-team seeding, just like the NCAA Tournament:

Seed 1 plays Seed 64

Seed 2 plays Seed 63

Seed 1 and Seed 2 can only meet in the championship

Seed 1 meets winners of (32 vs 33) in the second round

Seed 1 & Seed 4 are placed to meet in the regional semifinal

Seed 1 & Seed 8 are placed to meet in the regional quarterfinal

The bracket is generated recursively using the standard algorithm:

seed_order(64):
    [1,64, 32,33, 16,49, 17,48, 8,57, 25,40, ...]


These positions define the Round-of-64 games (g1–g32).
Later rounds are built by pairing winners of adjacent games automatically.

🎲 Team Strength Distributions

Each team 
i
i receives a stochastic strength value 
vi∈(0,1)
v
i
	​

∈(0,1) drawn from a distribution:

Seeds 1–16:
High-mean, low-variance Beta distributions (“stable favorites”).

Seeds 17–32:
Medium-variance Beta distributions (“volatile middle teams”).

Seeds 33–64:
Bimodal mixtures of two Betas (“boom-or-bust” teams).
Sometimes very strong, sometimes very weak.

These distributions ensure a realistic diversity in upset rates.

⚔️ Match Outcome Rule

In every individual game:

P(i wins)=vivi+vj.
P(i wins)=
v
i
	​

+v
j
	​

v
i
	​

	​

.

This ensures:

better teams win more often

but underdogs always have a chance

🧮 Scoring System

Each correctly predicted winner earns points:

Round	Games	Points per correct pick
Round 1	32	1
Round 2	16	2
Sweet 16	8	4
Elite 8	4	8
Final Four	2	16
Championship	1	32

Example:
If your bracket gets 6 picks right in the Sweet 16 → 
6×4=24
6×4=24 points.

🏆 Tournament-Level Scoring (Important)

For each simulated tournament:

Compute each bracket’s total weighted score.

Find the highest score 
S\*
S
\*
.

Let 
T
T be the set of brackets achieving that score.

Each bracket in 
T
T receives 1 / |T| points.

Examples:

One clear best bracket → gets 1 point

Three brackets tie for best → each gets 1/3 point

Ten brackets tie → each gets 0.1 points

A student’s final score is the sum of points across all their submitted brackets.

📥 Bracket Submission Format (brackets.csv)

Students submit brackets in a CSV file with the following columns:

student,bracket_name,g1,g2,...,g63


Each entry gk is a team seed number (1–64) corresponding to the predicted winner of game 
k
k.

There are 63 total games:

g1–g32: Round of 64

g33–g48: Round of 32

g49–g56: Sweet 16

g57–g60: Elite 8

g61–g62: Final Four

g63: Championship

The script validates that a bracket is structurally correct.

📝 Example Test File (brackets_test.csv)

Here is the example file included in the repo:

student,bracket_name,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15,g16,g17,g18,g19,g20,g21,g22,g23,g24,g25,g26,g27,g28,g29,g30,g31,g32,g33,g34,g35,g36,g37,g38,g39,g40,g41,g42,g43,g44,g45,g46,g47,g48,g49,g50,g51,g52,g53,g54,g55,g56,g57,g58,g59,g60,g61,g62,g63
alice,A,1,32,16,17,8,25,9,24,4,29,13,20,5,28,12,21,2,31,15,18,7,26,10,23,3,30,14,19,6,27,11,22,1,16,8,9,4,13,5,12,2,15,7,10,3,14,6,11,1,8,4,5,2,7,3,6,1,4,2,3,1,2,1
bob,A,64,33,49,48,57,40,56,24,61,36,52,45,60,37,53,44,63,34,50,47,58,39,55,42,62,35,51,46,59,38,54,43,64,49,57,56,61,52,60,53,63,50,58,55,62,51,59,54,64,57,61,60,63,58,62,59,64,61,63,62,64,63,64
charlie,A,64,33,49,48,57,25,56,41,4,55,52,20,5,51,53,21,63,47,50,45,7,26,23,42,3,39,14,37,6,30,11,43,64,16,8,56,36,12,37,21,63,50,39,55,3,46,6,11,1,8,52,12,63,21,3,59,1,9,17,25,1,17,1

🔍 How to Run

Install Python 3.9+.

Prepare a CSV file (brackets.csv or brackets_test.csv).

Run:

python tournament_competition.py


You will see:

a round-by-round textual comparison for one randomly generated tournament

bracket-level and student-level point totals based on many simulations

To change tournament count:

NUM_TOURNAMENTS = 10**6
