def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int | None = None, high: int | None = None):
    """
    Parse user input into an int guess.

    If low and high are given, the guess must fall within that inclusive range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: reject guesses outside the difficulty's range
    if low is not None and high is not None and (value < low or value > high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome: "Win", "Too High", or "Too Low"

    Both arguments must be ints; anything else raises TypeError.
    """
    # FIX: raise a readable TypeError on non-int input instead of falling back to string comparison
    if type(guess) is not int or type(secret) is not int:
        raise TypeError(
            "check_guess expects int guess and int secret, "
            f"got {type(guess).__name__} and {type(secret).__name__}"
        )

    if guess == secret:
        return "Win", "🎉 Correct!"
    # FIX: hints were backward; a high guess now says go LOWER and a low guess says go HIGHER
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
