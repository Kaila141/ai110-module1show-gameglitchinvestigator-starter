import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
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
