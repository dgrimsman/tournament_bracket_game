import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple


# =========================
# Global constants
# =========================

NUM_TEAMS = 64
NUM_GAMES = NUM_TEAMS - 1  # 63

# Games per round and scoring weights
ROUND_SIZES = [32, 16, 8, 4, 2, 1]
ROUND_WEIGHTS = [1, 2, 4, 8, 16, 32]


# =========================
# Team strength distributions
# =========================

@dataclass
class TeamDist:
    kind: str               # "beta" or "bimodal_beta"
    params: Tuple[float, ...]


def interpolate_mean(rank_index: int,
                     num_teams: int,
                     top_mean: float = 0.8,
                     bottom_mean: float = 0.3) -> float:
    """
    rank_index: 0 = best seed, num_teams-1 = worst seed
    Return a mean between top_mean and bottom_mean, monotone in rank.
    """
    t = rank_index / (num_teams - 1)
    return top_mean * (1 - t) + bottom_mean * t


def make_team_distributions(num_teams: int) -> List[TeamDist]:
    """
    Create heterogeneous team distributions.

    - Teams 1–16 (indices 0–15): stable strong (high mean, low variance) Beta
    - Teams 17–32 (16–31): volatile (medium variance) Beta
    - Teams 33–64 (32–63): bimodal Beta mixtures (boom/bust)
    """
    dists: List[TeamDist] = []

    for i in range(num_teams):
        base_mean = interpolate_mean(i, num_teams)

        if i < 16:
            # Stable: high concentration Beta
            concentration = 40.0
            alpha = base_mean * concentration
            beta = (1 - base_mean) * concentration
            dists.append(TeamDist("beta", (alpha, beta)))

        elif i < 32:
            # Volatile: lower concentration Beta
            concentration = 10.0
            alpha = base_mean * concentration
            beta = (1 - base_mean) * concentration
            dists.append(TeamDist("beta", (alpha, beta)))

        else:
            # Bimodal mixture of two Betas: one below, one above base_mean
            spread = 0.35
            low_mean = max(0.01, base_mean - spread / 2)
            high_mean = min(0.99, base_mean + spread / 2)

            conc_mode = 15.0
            a1 = low_mean * conc_mode
            b1 = (1 - low_mean) * conc_mode
            a2 = high_mean * conc_mode
            b2 = (1 - high_mean) * conc_mode

            # params: alpha1, beta1, alpha2, beta2, mixing_weight_for_mode2
            dists.append(TeamDist("bimodal_beta", (a1, b1, a2, b2, 0.5)))

    return dists


TEAM_DISTS = make_team_distributions(NUM_TEAMS)


def sample_team_values(rng: random.Random) -> List[float]:
    """
    Sample v_i in [0,1] for each team i from its (possibly bimodal) distribution.
    """
    values: List[float] = []
    for d in TEAM_DISTS:
        if d.kind == "beta":
            alpha, beta = d.params
            v = rng.betavariate(alpha, beta)
        elif d.kind == "bimodal_beta":
            a1, b1, a2, b2, p2 = d.params
            if rng.random() < p2:
                v = rng.betavariate(a2, b2)
            else:
                v = rng.betavariate(a1, b1)
        else:
            raise ValueError(f"Unknown distribution kind: {d.kind}")
        values.append(v)
    return values


# =========================
# Bracket structure (proper seeding)
# =========================

def seed_order(n: int) -> List[int]:
    """
    Standard bracket seeding for n teams so that:
      - 1 plays n in Round 1,
      - 2 plays n-1,
      - 1 and 2 can only meet in the final, etc.

    Returns a list of 1-based seed numbers giving their positions
    from top to bottom of the bracket.
    """
    if n == 1:
        return [1]
    half = n // 2
    prev = seed_order(half)
    mirror = [n + 1 - x for x in prev]
    out: List[int] = []
    for a, b in zip(prev, mirror):
        out.extend([a, b])
    return out


def initial_round_order() -> List[int]:
    """
    Return the order of teams in the Round of 64 according to standard seeding.

    Example for first few games (seeds):
      g1:  1 vs 64
      g2: 32 vs 33
      g3: 16 vs 49
      g4: 17 vs 48
      g5:  8 vs 57
      g6: 25 vs 40
      ...

    Internally we use 0-based team indices, so we subtract 1.
    """
    seed_positions = seed_order(NUM_TEAMS)   # 1-based seeds
    return [s - 1 for s in seed_positions]   # convert to 0-based team indices


# =========================
# Tournament simulation
# =========================

def simulate_tournament(team_values: List[float],
                        rng: random.Random) -> List[int]:
    """
    Simulate one tournament with seeded bracket.

    - Teams are 0..63
    - First round uses initial_round_order().
    - Each game: i beats j with probability v_i / (v_i + v_j).
    - Returns list of length 63 of winning team indices per game.
    """
    if len(team_values) != NUM_TEAMS:
        raise ValueError("team_values must have length 64")

    winners_all_games: List[int] = []
    current_round = initial_round_order()

    while len(current_round) > 1:
        next_round = []
        for k in range(0, len(current_round), 2):
            i = current_round[k]
            j = current_round[k + 1]
            vi = team_values[i]
            vj = team_values[j]
            p_i_wins = vi / (vi + vj)
            winner = i if rng.random() < p_i_wins else j
            winners_all_games.append(winner)
            next_round.append(winner)
        current_round = next_round

    assert len(winners_all_games) == NUM_GAMES
    return winners_all_games


# =========================
# Bracket validation & scoring
# =========================

def validate_bracket(winners: List[int]) -> None:
    """
    Check that a bracket (list of length 63 of team indices 0..63) is
    consistent with the seeded bracket structure.

    Raises ValueError if inconsistent or mis-sized.
    """
    if len(winners) != NUM_GAMES:
        raise ValueError(f"Bracket must have {NUM_GAMES} entries")

    idx = 0
    current_round = initial_round_order()

    while len(current_round) > 1:
        next_round = []
        for k in range(0, len(current_round), 2):
            if idx >= len(winners):
                raise ValueError("Bracket ended too early")

            i = current_round[k]
            j = current_round[k + 1]
            w = winners[idx]
            idx += 1

            if w not in (i, j):
                raise ValueError(
                    f"Inconsistent bracket: predicted winner team {w + 1} "
                    f"is not in this game (teams {i + 1} vs {j + 1})."
                )
            next_round.append(w)
        current_round = next_round

    if idx != NUM_GAMES:
        raise ValueError("Bracket has extra entries after the tournament ends")


def score_bracket(bracket_winners: List[int],
                  actual_winners: List[int]) -> int:
    """
    Weighted scoring:
    - Round 1 (games 1–32): 1 point each
    - Round 2 (games 33–48): 2 points each
    - Round 3 (games 49–56): 4 points each
    - Round 4 (games 57–60): 8 points each
    - Round 5 (games 61–62): 16 points each
    - Round 6 (game 63): 32 points

    Returns total score.
    """
    if len(bracket_winners) != NUM_GAMES or len(actual_winners) != NUM_GAMES:
        raise ValueError(f"Both winner lists must have length {NUM_GAMES}")

    score = 0
    idx = 0
    for r_size, w in zip(ROUND_SIZES, ROUND_WEIGHTS):
        for _ in range(r_size):
            if bracket_winners[idx] == actual_winners[idx]:
                score += w
            idx += 1
    return score


# =========================
# Reading student brackets
# =========================

def read_brackets_from_csv(path: str) -> List[Dict]:
    """
    Reads brackets from CSV with columns:

    student,bracket_name,g1,...,g63

    Each gk is a team ID 1..64.

    Returns list of dicts:
    {
        "student": <str>,
        "bracket_name": <str>,
        "winners": [int team indices 0..63, length 63]
    }
    """
    brackets: List[Dict] = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        expected_cols = [f"g{i}" for i in range(1, NUM_GAMES + 1)]

        for row in reader:
            for col in ["student", "bracket_name"]:
                if col not in row:
                    raise ValueError(f"Missing column '{col}' in CSV header")

            winners: List[int] = []
            for col in expected_cols:
                if col not in row:
                    raise ValueError(f"Missing column '{col}' in CSV header")
                try:
                    team_id_1based = int(row[col])
                    if not (1 <= team_id_1based <= NUM_TEAMS):
                        raise ValueError
                    winners.append(team_id_1based - 1)  # store 0-based
                except Exception:
                    raise ValueError(
                        f"Invalid team id in column {col} for student "
                        f"{row['student']} bracket {row['bracket_name']}: "
                        f"got '{row[col]}'"
                    )

            # Validate bracket consistency
            try:
                validate_bracket(winners)
            except ValueError as e:
                raise ValueError(
                    f"Invalid bracket for student {row['student']} "
                    f"bracket {row['bracket_name']}: {e}"
                )

            brackets.append(
                {
                    "student": row["student"],
                    "bracket_name": row["bracket_name"],
                    "winners": winners,
                }
            )

    if not brackets:
        raise ValueError("No brackets read from CSV")
    return brackets


# =========================
# Running the competition
# =========================

def run_competition(
    brackets: List[Dict],
    num_tournaments: int = 10**6,
    seed: int = 0,
) -> Tuple[Dict[Tuple[str, str], float], Dict[str, float]]:
    """
    Run many tournament simulations and score brackets.

    For each tournament:
        - compute all bracket scores
        - let S* be the highest score
        - let T be the set of brackets achieving S*
        - each bracket in T receives 1 / |T| points

    Returns:
    - bracket_wins: (student, bracket_name) -> total points (may be fractional)
    - student_wins: student -> total points (sum over their brackets)
    """
    rng = random.Random(seed)

    bracket_keys = [(b["student"], b["bracket_name"]) for b in brackets]
    bracket_wins: Dict[Tuple[str, str], float] = {key: 0.0 for key in bracket_keys}

    for _ in range(num_tournaments):
        # 1. Sample team values and simulate tournament
        team_values = sample_team_values(rng)
        actual_winners = simulate_tournament(team_values, rng)

        # 2. Score each bracket
        scores: List[int] = []
        for b in brackets:
            s = score_bracket(b["winners"], actual_winners)
            scores.append(s)

        max_score = max(scores)
        best_indices = [i for i, s in enumerate(scores) if s == max_score]

        # 3. Split 1 point among all tied top brackets
        points_each = 1.0 / len(best_indices)
        for idx_winner in best_indices:
            key = bracket_keys[idx_winner]
            bracket_wins[key] += points_each

    # Aggregate by student
    student_wins: Dict[str, float] = defaultdict(float)
    for (student, _bname), wins in bracket_wins.items():
        student_wins[student] += wins

    return bracket_wins, student_wins


# =========================
# Text viewer for one tournament vs one bracket
# =========================

def view_tournament_vs_bracket(
    team_values: List[float],
    actual_winners: List[int],
    bracket_winners: List[int],
    student: str = "student",
    bracket_name: str = "A",
) -> None:
    """
    Pretty-print a single simulated tournament bracket, comparing it
    against one student's bracket.

    Shows each game with:
        - seeds and drawn v_i
        - actual winner
        - student's predicted winner
        - correctness mark
        - points earned per round
    """
    if len(team_values) != NUM_TEAMS:
        raise ValueError("team_values must have length 64")
    if len(actual_winners) != NUM_GAMES or len(bracket_winners) != NUM_GAMES:
        raise ValueError(f"Winner lists must have length {NUM_GAMES}")

    print(f"=== Tournament vs Bracket: {student} [{bracket_name}] ===\n")

    idx = 0
    current_round = initial_round_order()
    total_points = 0
    round_number = 1

    for r_size, w in zip(ROUND_SIZES, ROUND_WEIGHTS):
        print(f"--- Round {round_number} (weight {w} per correct pick) ---")
        round_points = 0
        next_round = []

        for g in range(r_size):
            i = current_round[2 * g]
            j = current_round[2 * g + 1]

            actual = actual_winners[idx]
            predicted = bracket_winners[idx]

            correct = (actual == predicted)
            if correct:
                round_points += w
                mark = "✓"
            else:
                mark = "✗"

            seed_i = i + 1
            seed_j = j + 1
            seed_actual = actual + 1
            seed_pred = predicted + 1

            print(
                f"G{idx + 1:2d}: "
                f"Seed {seed_i:2d} (v={team_values[i]:.3f}) vs "
                f"Seed {seed_j:2d} (v={team_values[j]:.3f})  "
                f"--> actual: Seed {seed_actual:2d}, "
                f"predicted: Seed {seed_pred:2d}  [{mark}]"
            )

            next_round.append(actual)
            idx += 1

        total_points += round_points
        print(f"Round {round_number} points: {round_points}\n")

        current_round = next_round
        round_number += 1

    print(f"TOTAL POINTS for {student} [{bracket_name}]: {total_points}")
    print("==============================================\n")


# =========================
# Helper: print mapping of games to seeds
# =========================

def print_bracket_mapping() -> None:
    """
    Print which seeds can appear in each game g1..g63, using the seeded
    initial round. This is useful to give to students as a reference.
    """
    game_index = 1
    round_num = 1
    current_slots = [[i] for i in initial_round_order()]

    while len(current_slots) > 1:
        print(f"Round {round_num}:")
        next_slots = []
        for k in range(0, len(current_slots), 2):
            left = current_slots[k]
            right = current_slots[k + 1]
            left_seeds = [s + 1 for s in left]
            right_seeds = [s + 1 for s in right]
            print(f"  g{game_index}: teams {left_seeds} vs {right_seeds}")
            next_slots.append(left + right)
            game_index += 1
        current_slots = next_slots
        round_num += 1
    print()


# =========================
# Main
# =========================

if __name__ == "__main__":
    # Path to CSV with student brackets
    brackets_path = "test_brackets.csv"  # change to "brackets_test.csv" for testing

    # Read and validate all brackets
    brackets = read_brackets_from_csv(brackets_path)

    # Example: inspect one tournament vs one bracket
    rng_demo = random.Random(123)
    demo_values = sample_team_values(rng_demo)
    demo_actual = simulate_tournament(demo_values, rng_demo)

    example_bracket = brackets[0]
    view_tournament_vs_bracket(
        demo_values,
        demo_actual,
        example_bracket["winners"],
        student=example_bracket["student"],
        bracket_name=example_bracket["bracket_name"],
    )

    # Run full competition
    NUM_TOURNAMENTS = 100  # maybe reduce for quick testing
    bracket_wins, student_wins = run_competition(
        brackets,
        num_tournaments=NUM_TOURNAMENTS,
        seed=0,
    )

    print("Bracket points (tournaments' points split among ties):")
    for (student, bname), wins in sorted(
        bracket_wins.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {student} [{bname}]: {wins:.3f}")

    print("\nStudent leaderboard (total points over all brackets):")
    for student, wins in sorted(
        student_wins.items(), key=lambda kv: kv[1], reverse=True
    ):
        print(f"  {student}: {wins:.3f}")
