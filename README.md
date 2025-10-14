# Tic Tac Toe

Tic Tac Toe in the terminal. A technical challenge from a prospective employer.

## Features

- Input validation with feedback: only correct input is accepted. Input must be in the form [column, row], e.g. "B1".
- Help messages: guide the user to input in the correct format
- Emoji board: the game board is drawn with emojis because text is boring
- Win detection: checks across rows, columns, and diagonals
- Early draw prediction: predicts a draw when it's inevitable
- Game state feedback: announces winner and loser, or if game is a tie
- Entertaining messages to the user
- `exit` / `quit` / `:q` commands

## Running the Game

```
git clone https://github.com/its-all-waves/tic-tac-toe.git
cd tic-tac-toe
python3.12 main.py
```

> Python 3.12 or higher is required. A virtual environment is not necessary as there are no external dependencies.

> Tested on macOS, Debian 12. Windows 11's emoji set is differrent such that the game board does not render as intended.

## Running the Tests

```
cd tic-tac-toe
python3.12 -m unittest
```
