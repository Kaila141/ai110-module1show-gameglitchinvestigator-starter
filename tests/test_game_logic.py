import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    new_game_state,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, _ = check_guess(40, 50)
    assert result == "Too Low"

@pytest.mark.parametrize("raw", ["0", "-5", "101", "1000"])
def test_parse_guess_rejects_out_of_range_normal(raw):
    # Normal range is 1-100; anything outside must be rejected with a message
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is False
    assert value is None
    assert err == "Guess must be between 1 and 100."

@pytest.mark.parametrize("raw", ["1", "50", "100"])
def test_parse_guess_accepts_in_range_including_bounds(raw):
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is True
    assert value == int(raw)
    assert err is None

@pytest.mark.parametrize("difficulty,too_high", [("Easy", "21"), ("Hard", "51")])
def test_parse_guess_uses_difficulty_range(difficulty, too_high):
    # 21 is valid on Normal but must be rejected on Easy; 51 likewise on Hard
    low, high = get_range_for_difficulty(difficulty)
    ok, _, err = parse_guess(too_high, low, high)
    assert ok is False
    assert err == f"Guess must be between {low} and {high}."

def test_parse_guess_decimal_out_of_range_rejected():
    # "100.9" truncates to 100 (valid), but "101.5" truncates to 101 (invalid)
    assert parse_guess("100.9", 1, 100)[0] is True
    assert parse_guess("101.5", 1, 100)[0] is False

def test_parse_guess_non_numeric_still_reports_not_a_number():
    ok, value, err = parse_guess("abc", 1, 100)
    assert (ok, value, err) == (False, None, "That is not a number.")

def test_parse_guess_without_range_does_not_enforce_bounds():
    # Backward compatible: no low/high means no range check
    assert parse_guess("500") == (True, 500, None)

# --- check_guess: numeric comparison and type safety ---

def test_check_guess_compares_numerically_not_alphabetically():
    # As strings "9" > "50", which previously gave the wrong hint
    assert check_guess(9, 50)[0] == "Too Low"
    assert check_guess(100, 99)[0] == "Too High"

@pytest.mark.parametrize("guess,secret", [("50", 50), (50, "50"), ("50", "50"), (50.0, 50), (True, 1), (None, 50)])
def test_check_guess_rejects_non_int_arguments(guess, secret):
    with pytest.raises(TypeError, match="check_guess expects int"):
        check_guess(guess, secret)

def test_check_guess_type_error_message_names_the_types():
    with pytest.raises(TypeError, match="got str and int"):
        check_guess("50", 50)

# --- update_score ---

@pytest.mark.parametrize("attempt,expected", [(1, 100), (2, 90), (5, 60), (9, 20), (10, 10)])
def test_win_points_drop_ten_per_attempt(attempt, expected):
    # First-try win is worth exactly 100 (no off-by-one on the attempt number)
    assert update_score(0, "Win", attempt) == expected

@pytest.mark.parametrize("attempt", [11, 20, 1000])
def test_win_points_never_below_ten(attempt):
    assert update_score(0, "Win", attempt) == 10

def test_win_adds_to_existing_score():
    assert update_score(-15, "Win", 1) == 85

@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2, 3, 4, 7, 8])
def test_wrong_guess_always_deducts_five(outcome, attempt):
    # Previously "Too High" added 5 on even attempts
    assert update_score(50, outcome, attempt) == 45

def test_high_and_low_deduct_the_same_amount():
    for attempt in range(1, 9):
        assert update_score(30, "Too High", attempt) == update_score(30, "Too Low", attempt)

def test_wrong_guesses_never_increase_score():
    score = 0
    for attempt in range(1, 9):
        new_score = update_score(score, "Too High" if attempt % 2 == 0 else "Too Low", attempt)
        assert new_score < score
        score = new_score

def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Bogus", 3) == 42

def test_full_round_score():
    # Two misses then a win on attempt 3: -5 -5 +80
    score = update_score(0, "Too Low", 1)
    score = update_score(score, "Too High", 2)
    score = update_score(score, "Win", 3)
    assert score == 70

# --- new_game_state ---

@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_new_game_secret_always_within_difficulty_range(difficulty):
    # Previously New Game used a hardcoded 1-100 regardless of difficulty
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(200):
        assert low <= new_game_state(low, high)["secret"] <= high

def test_new_game_secret_can_hit_both_bounds():
    secrets = {new_game_state(1, 3)["secret"] for _ in range(200)}
    assert secrets == {1, 2, 3}

def test_new_game_state_resets_all_progress():
    state = new_game_state(1, 20)
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []

def test_new_game_state_history_is_not_shared_between_rounds():
    first = new_game_state(1, 20)
    first["history"].append(7)
    assert new_game_state(1, 20)["history"] == []

def test_new_game_state_single_value_range():
    assert new_game_state(5, 5)["secret"] == 5
