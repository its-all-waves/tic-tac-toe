import time
import copy
from typing import Literal

X = "X"
O = "O"

type PlayerSign = Literal["X", "O"]

type BoardEmoji = Literal["❌", "⭕", "⬜"]

BOARD_EMOJI: dict[PlayerSign | None, BoardEmoji] = {
    X: "❌",
    O: "⭕",
    None: "⬜",
}


class Board:
    # fmt: off
    # map user-entered coord to board index
    _MOVE_MAP: dict[str, int] = {
        "A": 0, "B": 1, "C": 2,
        "a": 0, "b": 1, "c": 2,
        "1": 0, "2": 1, "3": 2,
    }
    # fmt: on

    _b: list[list[None | PlayerSign]]

    def __init__(self):
        self._b = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def _is_move_valid(self, move: str) -> bool:
        if len(move) != 2:
            return False
        col, row = move
        if col not in ("A", "B", "C", "a", "b", "c"):
            return False
        if row not in ("1", "2", "3"):
            return False
        return True

    def _is_move_available(self, i: int, j: int) -> bool:
        return not bool(self._b[i][j])

    type MarkResult = Literal[
        "INVALID_INPUT",
        "MOVE_UNAVAILABLE",
        "MOVE_APPLIED",
    ]

    def mark(self, player: PlayerSign, move: str) -> MarkResult:
        if not self._is_move_valid(move):
            return "INVALID_INPUT"
        col, row = move
        i, j = self._MOVE_MAP[row], self._MOVE_MAP[col]
        if not self._is_move_available(i, j):
            return "MOVE_UNAVAILABLE"
        self._b[i][j] = player
        return "MOVE_APPLIED"

    type GameState = Literal[
        "GAME_IN_PROGRESS",
        "PLAYER_IS_WINNER",
        "TIE",
    ]

    def is_game_over(self, curr_player: PlayerSign) -> GameState:
        # check for win across rows
        for row in self._b:
            if row[0] == row[1] == row[2] == curr_player:
                return "PLAYER_IS_WINNER"

        # check for win across cols
        for j in range(3):
            if self._b[0][j] == self._b[1][j] == self._b[2][j] == curr_player:
                return "PLAYER_IS_WINNER"

        # check for win across diags
        if (
            self._b[0][0] == self._b[1][1] == self._b[2][2] == curr_player
            or self._b[2][0] == self._b[1][1] == self._b[0][2] == curr_player
        ):
            return "PLAYER_IS_WINNER"

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
        empty_cells = [
            (i, j) for i in range(3) for j in range(3) if self._b[i][j] is None
        ]
        if len(empty_cells) == 0:
            return "TIE"

        if len(empty_cells) == 1:
            # predict tie or win from next (final) move
            next_player = X if curr_player == O else O
            board_copy = copy.deepcopy(self)
            i, j = empty_cells[0]
            board_copy._b[i][j] = next_player
            state_after_next_move = board_copy.is_game_over(next_player)
            match state_after_next_move:
                case "PLAYER_IS_WINNER":
                    # let them make the winning move -- more fun/satisfying
                    return "GAME_IN_PROGRESS"
                case "TIE":
                    # next move will fill the board and not win the game, thus it's a tie
                    return "TIE"

        return "GAME_IN_PROGRESS"

    def print(self):
        p = [[BOARD_EMOJI[self._b[i][j]] for j in range(3)] for i in range(3)]
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

EXIT_CMDS = ("exit", "EXIT", "quit", "QUIT", ":q")

USER_MSG: dict[Literal["EXIT"] | Board.MarkResult, str] = {
    "EXIT": "So that's how it is... Ok... I see... Bye Felicia! 👋🏼",
    "INVALID_INPUT": "⚠️ Try again. Your move should look like this: B1 (letter, number)",
    "MOVE_UNAVAILABLE": "⚠️ Move is unavailable. Try again!",
}


def print_tie_seq():
    print("No one. No won won. Wait... No one... won. Whatever.\n")
    time.sleep(2)
    print("...so lame. Bye! 👋🏼\n")
    time.sleep(2)


def print_winner_seq(winner: PlayerSign, loser: PlayerSign):
    print(f"🎉 🍻   {BOARD_EMOJI[winner]}   🥳 🍾\n")
    time.sleep(1)
    print(f"🙌 Niiiice. Good job {BOARD_EMOJI[winner]} ! 💪\n")
    time.sleep(1.5)
    print(
        f"{BOARD_EMOJI[loser]}, how the heck do you lose at Tic Tac Toe? 👎 \n"
    )
    time.sleep(1.5)
    print("Seriously, you must be dense... 👎\n")
    time.sleep(1)
    print("Thanks for playing! Goodbye! 👋🏼\n")
    time.sleep(1)


def print_game_over_seq(winner: None | PlayerSign):
    print("GAME OVER!\n")
    time.sleep(1.5)
    print("🥁 And the winner is... 🥁\n")
    time.sleep(1.5)
    if winner:
        print_winner_seq(winner, loser=X if winner == O else O)
        return
    print_tie_seq()


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
            move = input(f"Mark {BOARD_EMOJI[curr_player]} at: ").strip()
            if move in EXIT_CMDS:
                print("\n" + USER_MSG["EXIT"] + "\n")
                exit()
            mark_result = board.mark(curr_player, move)
            match mark_result:
                case "INVALID_INPUT" | "MOVE_UNAVAILABLE":
                    print(USER_MSG[mark_result] + "\n")
                    continue
                case "MOVE_APPLIED":
                    break

        board.print()

        state = board.is_game_over(curr_player)
        match state:
            case "GAME_IN_PROGRESS":
                curr_player = X if curr_player == O else O
                continue
            case "PLAYER_IS_WINNER":
                winner = curr_player
                break
            case "TIE":
                break

    print_game_over_seq(winner)


if __name__ == "__main__":
    main()
