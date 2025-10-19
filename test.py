import unittest
from main import Board, X, O

_ = None


class TestIsGameOver(unittest.TestCase):
    def test_empty_board(self):
        board = Board()
        board._b = [
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ]
        # X goes 1st
        game_is_over = board.is_game_over(X)
        self.assertFalse(game_is_over)

    def test_game_not_over(self):
        board = Board()
        board._b = [
            [O, O, _],
            [X, O, X],
            [X, _, X],
        ]
        x_won = board.is_game_over(X)
        self.assertFalse(x_won)

        board = Board()
        board._b = [
            [O, X, _],
            [_, X, O],
            [X, O, _],
        ]
        o_won = board.is_game_over(O)
        self.assertFalse(o_won)

    def test_X_or_O_wins(self):
        board = Board()
        board._b = [
            [X, X, X],
            [_, O, O],
            [_, _, _],
        ]
        x_won = board.is_game_over(X)
        self.assertTrue(x_won)

        board = Board()
        board._b = [
            [_, O, _],
            [X, O, X],
            [X, O, _],
        ]
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

    def test_detects_win_in_rows(self):
        board = Board()
        board._b = [
            [X, X, X],
            [X, O, _],
            [_, O, O],
        ]
        x_won = board.is_game_over(X)
        self.assertTrue(x_won)

        board = Board()
        board._b = [
            [X, X, O],
            [O, O, O],
            [X, _, X],
        ]
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

        board = Board()
        board._b = [
            [_, X, _],
            [_, X, X],
            [O, O, O],
        ]
        # O just played
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

    def test_detects_win_in_cols(self):
        board = Board()
        board._b = [
            [O, _, X],
            [O, X, X],
            [O, _, _],
        ]
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

        board = Board()
        board._b = [
            [O, X, _],
            [_, X, _],
            [_, X, O],
        ]
        x_won = board.is_game_over(X)
        self.assertTrue(x_won)

        board = Board()
        board._b = [
            [_, _, O],
            [X, X, O],
            [_, X, O],
        ]
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

    def test_detects_win_in_diags(self):
        board = Board()
        board._b = [
            [_, _, X],
            [O, X, O],
            [X, _, _],
        ]
        x_won = board.is_game_over(X)
        self.assertTrue(x_won)

        board = Board()
        board._b = [
            [O, X, _],
            [_, O, X],
            [X, _, O],
        ]
        o_won = board.is_game_over(O)
        self.assertTrue(o_won)

    def test_tied_board_full(self):
        board = Board()
        board._b = [
            [O, X, O],
            [X, O, X],
            [X, O, X],
        ]
        x_won = board.is_game_over(X)
        self.assertIsNone(x_won)

    def test_tied_board_not_full(self):
        board = Board()
        board._b = [
            [X, O, O],
            [O, _, X],
            [X, X, O],
        ]
        # O just played, next move (X's) will result in a tie
        o_won = board.is_game_over(O)
        self.assertIsNone(o_won)

        board = Board()
        board._b = [
            [X, _, O],
            [O, O, X],
            [X, O, X],
        ]
        # O just played, next move (X's) will result in a tie
        o_won = board.is_game_over(O)
        self.assertIsNone(o_won)

if __name__ == "__main__":
    unittest.main()
