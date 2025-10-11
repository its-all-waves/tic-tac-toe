from typing import Literal

type PlayerSign = Literal["x", "o"]

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


class Board:
    empty = "⬜"

    b: list[list[str]] = [
        [empty, empty, empty],
        [empty, empty, empty],
        [empty, empty, empty],
    ]

    def print(self):
        b = self.b
        print()
        print("  A  B  C")
        print("1", b[0][0], b[0][1], b[0][2])
        print("2", b[1][0], b[1][1], b[1][2])
        print("3", b[2][0], b[2][1], b[2][2])
        print()



def main():
    board = Board()
    board.print()


if __name__ == "__main__":
    main()
