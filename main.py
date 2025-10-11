from typing import Literal

type PlayerSign = Literal["X", "O"]

type PlayerEmoji = Literal["❌", "⭕"]


class Player:
    sign: PlayerSign
    emoji: PlayerEmoji

    def __init__(self, sign):
        self.sign = sign
        if sign == "x":
            self.emoji = "❌"
            return
        self.emoji = "⭕"

    def __repr__(self):
        return self.emoji


type EmptyEmoji = Literal["⬜"]


class Board:
    empty: EmptyEmoji = "⬜"

    b: list[list[EmptyEmoji | PlayerEmoji]] = [
        [empty, empty, empty],
        [empty, empty, empty],
        [empty, empty, empty],
    ]

    def add_move(self, turn: PlayerSign, coords: tuple[int, int]):
        col, row = coords
        self.b[row][col] = sign_map[turn]

    def print(self):
        b = self.b
        print()
        print("  A  B  C")
        print("1", b[0][0], b[0][1], b[0][2])
        print("2", b[1][0], b[1][1], b[1][2])
        print("3", b[2][0], b[2][1], b[2][2])
        print()


player_turn: PlayerSign = "X"

rules = """
[ Rules ]

⇢ X goes first.

⇢ Enter coordinates as [X, Y] or [column, row]. For example, to make your move at column 3, row 2, enter 'C2'.

⇢ Case does not matter.
"""


def isInputValid(inp: str) -> bool:
    inp = inp.strip()
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

sign_map: dict[PlayerSign, PlayerEmoji] = {
    "X": "❌",
    "O": "⭕",
}


def main():
    # wait for user to confirm understanding of rules
    print(rules)
    while True:
        if input("Capisce? Press enter to play!") == "":
            break

    board = Board()
    board.print()

    # wait for valid input
    move: str
    while True:
        move = input(f"Make a move (e.g. B3).\n{player_turn} at: ")
        if isInputValid(move):
            break

    col, row = move
    board.add_move(player_turn, coords=(move_map[col], move_map[row]))
    board.print()


if __name__ == "__main__":
    main()
