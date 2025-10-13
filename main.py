import time
import copy
from typing import Literal

X = "X"
O = "O"

type PlayerSign = Literal["X", "O"]

type BoardEmoji = Literal["❌", "⭕", "⬜"]

PLAYER_EMOJI_MAP: dict[PlayerSign | None, BoardEmoji] = {
    X: "❌",
    O: "⭕",
    None: "⬜",
}


class Board:
    b: list[list[None | PlayerSign]]

    def __init__(self):
        self.b = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def mark(self, turn: PlayerSign, coords: tuple[int, int]):
        j, i = coords
        self.b[i][j] = turn

    def is_move_available(self, coord) -> bool:
        j, i = coord
        return not bool(self.b[i][j])

    def print(self):
        p: list[list[None | BoardEmoji]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        for i in range(3):
            for j in range(3):
                p[i][j] = PLAYER_EMOJI_MAP[self.b[i][j]]
        print()
        print("  A  B  C")
        print("1", *p[0])
        print("2", *p[1])
        print("3", *p[2])
        print()


RULES = """
❌❌❌ Tic Tac Toe ⭕⭕⭕

📏 RULES 📐

❌ goes first.

📍 Enter coordinates as [X, Y] or [column, row] to make your move.
   For example, to make your move at column 3, row 2, enter "C2" or "c2".
   "2C" won't work.

🚪 To quit once the game is going, type "exit" or "quit".
   (If you're a Vim user, you know what to do.)

🐟 Capisce? Press enter to play!"""


# fmt: off
# map user-entered coord to board index
MOVE_MAP: dict[str, int] = {
    "A": 0, "B": 1, "C": 2,
    "a": 0, "b": 1, "c": 2,
    "1": 0, "2": 1, "3": 2,
}
# fmt: on


def is_input_valid(inp: str) -> bool:
    if len(inp) != 2:
        return False
    col, row = inp
    if col not in ("A", "B", "C", "a", "b", "c"):
        return False
    if row not in ("1", "2", "3"):
        return False
    return True


def is_game_over(curr_player: PlayerSign, board: Board) -> bool | None:
    """
    Returns:
        - `True` if `curr_player` won the game
        - `False` if the game is not over
        - `None` if it's a tie
    """
    # check for win across rows
    for row in board.b:
        if row[0] == row[1] == row[2] == curr_player:
            return True

    # check for win across cols
    for j in range(3):
        if board.b[0][j] == board.b[1][j] == board.b[2][j] == curr_player:
            return True

    # check for win across diags
    if (
        board.b[0][0] == board.b[1][1] == board.b[2][2] == curr_player
        or board.b[2][0] == board.b[1][1] == board.b[0][2] == curr_player
    ):
        return True

    # It's possible to detect a tie or win before the last move is made.
    # e.g. tie - X's turn, X cannot win, only possible move results in a draw
    #
    #     X  O  O
    #     O  _  X
    #     X  X  O
    #
    # e.g. win - X's turn, only possible move is a win
    #
    #     X  O  O
    #     O  X  X
    #     X  O  _  <- X wins

    # check for tie
    is_board_full = True
    empty_cells: list[tuple[int, int]] = []
    for i in range(3):
        for j in range(3):
            if board.b[i][j] is None:
                is_board_full = False
                empty_cells.append((i, j))
    if is_board_full:
        return None

    if len(empty_cells) == 1:
        # predict tie or win from next (final) move
        next_player = X if curr_player == O else O
        board_copy = copy.deepcopy(board)
        i, j = empty_cells[0]
        board_copy.b[i][j] = next_player
        will_next_player_win = is_game_over(next_player, board_copy)
        if will_next_player_win:
            # let them make the winning move -- more fun/satisfying
            return False
        if will_next_player_win is None:
            # next move will fill the board and not win the game, thus it's a tie
            return None

    return False


def main():
    # wait for user to confirm understanding of rules
    print(RULES, end="")
    _ = input()

    board = Board()
    board.print()

    curr_player: PlayerSign = X
    winner: None | PlayerSign = None

    while True:
        # wait for a valid move to be applied
        while True:
            move = input(f"Mark {PLAYER_EMOJI_MAP[curr_player]} at: ").strip()
            if move in ("exit", "EXIT", "quit", "QUIT", ":q"):
                print("So that's how it is... Ok... I see... Bye Felicia! 👋🏼")
                time.sleep(1.5)
                exit()
            if not is_input_valid(move):
                print(
                    "⚠️ Try again. Your move should look like this: B1 (letter, number)\n"
                )
                continue
            col, row = move
            coords = (MOVE_MAP[col], MOVE_MAP[row])
            if not board.is_move_available(coords):
                print("⚠️ Move is unavailable. Try again!\n")
                continue
            board.mark(curr_player, coords)
            break

        board.print()

        curr_player_won = is_game_over(curr_player, board)
        if curr_player_won:
            winner = curr_player
            break
        if curr_player_won is None:
            break

        curr_player = X if curr_player == O else O

    print("GAME OVER!\n")
    time.sleep(1.5)
    print("🥁 And the winner is... 🥁\n")
    time.sleep(1.5)

    if winner:
        loser = X if winner == O else O
        print(f"🎉 🍻   {PLAYER_EMOJI_MAP[winner]}   🥳 🍾\n")
        time.sleep(1)
        print(f"🙌 Niiiice. Good job {PLAYER_EMOJI_MAP[winner]}! 💪\n")
        time.sleep(1.5)
        print(
            f"{PLAYER_EMOJI_MAP[loser]}, how the heck do you lose at Tic Tac Toe? 👎 \n"
        )
        time.sleep(1.5)
        print("Seriously, you must be dense... 👎\n")
        time.sleep(1)
        print("Thanks for playing! Goodbye! 👋🏼\n")
        time.sleep(1)
        return

    print("No one. No won won. Wait... No one... won. Whatever.\n")
    time.sleep(2)
    print("...so lame. Bye! 👋🏼\n")
    time.sleep(2)


if __name__ == "__main__":
    main()
