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


def is_game_over(p: PlayerSign, board: Board) -> bool | None:
    """
    Returns:
        - `True` if player `p` won the game
        - `False` if the game is not over
        - `None` if it's a draw
    """
    # check for win across rows
    for row in board.b:
        if row[0] == row[1] == row[2] == p:
            return True
    # TODO: check across cols
    # TODO: check across diags
    # TODO: check for draw -- all cells filled? (or all but 1 or 2?)
    return False


def main():
    # wait for user to confirm understanding of rules
    print(rules, end="")
    _ = input()

    board = Board()
    board.print()

    # the current player
    player_turn: PlayerSign = X

    while True:
        # wait for a valid move to be applied
        while True:
            print("Make your move.")
            move = input(f"Mark {player_turn} at: ").strip()
            if not is_input_valid(move):
                # TODO: help message?
                continue
            col, row = move
            coords = (move_map[col], move_map[row])
            if not board.is_move_available(coords):
                print("⚠️ Move is unavailable. Try again!")
                continue
            board.mark(player_turn, coords)
            break

        board.print()

        # TODO: check if game over
        if is_game_over(player_turn, board):
            break
        player_turn = X if player_turn == O else O

    print("GAME ENDED. WINNER: ", player_turn)


if __name__ == "__main__":
    main()
