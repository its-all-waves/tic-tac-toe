import time
import copy
from typing import Literal

X = "X"
O = "O"

type PlayerSign = Literal["X", "O"]

type BoardEmoji = Literal["❌", "⭕", "⬜"]


class Board:
    b: list[list[None | PlayerSign]] = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    def mark(self, turn: PlayerSign, coords: tuple[int, int]):
        col, row = coords
        self.b[row][col] = turn

    def is_move_available(self, coord) -> bool:
        y, x = coord
        return not bool(self.b[x][y])

    emoji_map: dict[PlayerSign | None, BoardEmoji] = {
        X: "❌",
        O: "⭕",
        None: "⬜",
    }

    def print(self):
        p: list[list[None | BoardEmoji]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        for y in range(3):
            for x in range(3):
                p[y][x] = self.emoji_map[self.b[y][x]]
        print()
        print("  A  B  C")
        print("1", p[0][0], p[0][1], p[0][2])
        print("2", p[1][0], p[1][1], p[1][2])
        print("3", p[2][0], p[2][1], p[2][2])
        print()


rules = """
[ Rules ]

⇢ X goes first.

⇢ Enter coordinates as [X, Y] or [column, row]. For example, to make your move at column 3, row 2, enter 'C2'.

⇢ Case does not matter.

Capisce? Press enter to play!"""


def is_input_valid(inp: str) -> bool:
    if len(inp) != 2:
        return False
    if inp[0] not in ("A", "B", "C", "a", "b", "c"):
        return False
    if inp[1] not in ("1", "2", "3"):
        return False
    return True


# fmt: off
# map user-entered coord to board index
move_map: dict[str, int] = {
    "A": 0, "B": 1, "C": 2,
    "a": 0, "b": 1, "c": 2,
    "1": 0, "2": 1, "3": 2,
}
# fmt: on


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
        # predict tie from next (final) move
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
    print(rules, end="")
    _ = input()

    board = Board()
    board.print()

    # the current player
    curr_player: PlayerSign = X
    winner: None | PlayerSign = None

    while True:
        # wait for a valid move to be applied
        while True:
            print("Make your move.")
            move = input(f"Mark {curr_player} at: ").strip()
            if not is_input_valid(move):
                # TODO: help message?
                continue
            col, row = move
            coords = (move_map[col], move_map[row])
            if not board.is_move_available(coords):
                print("⚠️ Move is unavailable. Try again!")
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

    print(f"{winner} WON!" if winner else "IT'S A DRAW!")


if __name__ == "__main__":
    main()
