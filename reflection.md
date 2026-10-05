# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Answer: The game loads with a message in blue to guess a number between 1 and 100 with 7 attempts left. There's a sidebar with three difficulty modes, each with different ranges and number of allowed attempts. There is a developer debug info and inputs for me to play the game.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
Answer:
  * The hints were backwards (when I entered a lower number, I was told to guess lower; when I entered a higher number, I was told to go higher.)
  * It doesn't display an error when I enter a number outside the range.
  * The tip on the guess input says "Press Enter to apply", but pressing Enter does nothing.
  * Speaking of, when I change difficulties, it still tells me to guess a number between 1 and 100, and the numbers themselves are greater than the 20 or 50 bounds.
  * Then displayed score doesn't seem to make much sense. Assuming the max store is 100, then a correct guess on the first attempt should give 100 as the final score, but instead i got 70. I suspect the score calculations aren't done correctly, possibly based on the attempts used or the points deducted and when. It also seems to not work the same when I guess too high or low.
  * The attempts, score, and history in the debug log didn't update in real-time. it seemed to lag behind entries.
  * Starting a new game doesn't work. It loads a new number, but the hint will always say "You already won. Start a new game to play again." This might be because the history isn't cleared after a round. Changing difficulties doesn't fix this. Only reloading does because that's when the history is cleared.
  * A smaller range for hard mode doesn't seem too hard. 
  * Changing modes mid-round doesn't change anything but the difficulty. Only pressing New Game changes it
  * Sometimes guesses don't go through or get logged in the history..


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------| ------------------------|
| Guess: 10, Target: 62 | Hint: "Go HIGHER" | Hint: "Go LOWER" | none | app.py, check_guess() |
| Guess: -26 | Error: Number less than 1 | Hint: "Go LOWER" | none | app.py, parse_guess() |
| Difficulty: Normal, Guess: 150 | Error: Number greater than 100 | Hint: "Go HIGHER" | none | app.py, parse_guess() |
| Guess: 62, Target: 62, 3 past attempts (above) | Debug score: -15, You win... Final score: 45 | Debug score: -10, You win... Final score: 35  | none | app.py, update_score() |
| Difficulty: Easy, Guess: 50 | Error: Number greater than 20 | Hint: "Go HIGHER" | none | app.py, parse_guess() |
| Guess: 100, Target: 15 | Hint: "Go LOWER" | Hint: "Go HIGHER" | none | app.py, check_guess() |
| Guess: 57.9, Target: 57 | Hint: "Enter an integer/Go LOWER" | You win![etc] | none | app.py, parse_guess(), lines 21-27 |
| Guess: 58, Target: 58, First attempt | Debug score: 0, You win... Final score: 100 | Debug score: 0, You win... Final score: 70  | none | app.py, update_score() |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Answer: Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Answer: The fix for backwards hints was correct: simply swapped the hint messages (eg., for a too high guess, the message is "GO LOWER", etc). This was a simple fix so it wasn't difficult to verify.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Answer: There was a bug where the unnecessarily secret was converted to a string for even-numbered attempts. I asked it to correct the issue. It suggested to remove the try catch entirely and let the error fail on its own. I tweaked it to still catch the error so it's clarified on the console, and it suggested also adding a user-facing error message + display. I rejected this idea because it seemed like too much to do and nothing in the current scope mentions displaying a user error message on invalid inputs, especially since it would now only be thrown through programming error than something the user inputs.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Answer: I tested it the same way I tested the code at the start. If these manual tests as well as the pytest tests pass, then I consider it fixed. If it introduced another issue or only fixed one case, then it wasn't fixed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  Answer: 
  * The existing tests pass (tweaked only to take the first result of the output), and AI helped me create a new test to also test for cases where it would've failed if the string conversion was also fized.
  * I also reran the code and tested with values that are higher and lower than the secret.
- Did AI help you design or understand any tests? How?
  Answer: 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
