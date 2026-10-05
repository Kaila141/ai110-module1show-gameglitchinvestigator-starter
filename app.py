import streamlit as st

from logic_utils import (get_range_for_difficulty, new_game_state, parse_guess, check_guess, update_score)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# FIX: start a fresh round on first load and whenever the difficulty changes, so the secret
# always matches the range and attempts, score, history and status don't carry over
# (attempts also start at 0, not 1, so the first guess is attempt 1 and can score 100)
if st.session_state.get("difficulty") != difficulty:
    st.session_state.update(new_game_state(low, high))
    st.session_state.difficulty = difficulty

st.subheader("Make a guess")

st.info(
    # FIX: use the difficulty's low and high instead of a hardcoded 1 to 100
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# FIX: reserve the debug panel's spot here but fill it after the submit handler runs
# (render_debug_info below), so attempts, score and history no longer lag one click behind
debug_slot = st.container()


def render_debug_info():
    with debug_slot:
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


# FIX: input and submit button live in a form so pressing Enter submits the guess
# and the typed text always arrives together with the click
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game resets status, score, history and attempts too, and picks the secret
# from the current difficulty's range instead of a hardcoded 1 to 100
if new_game:
    st.session_state.update(new_game_state(low, high))
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_debug_info()
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        # FIX: only valid guesses use up an attempt (it was counted before validation)
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: always pass the integer secret (it was converted to a string on even attempts)
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_debug_info()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
