import unittest
from main import Board, is_game_over, X, O

_ = None


class TestIsGameOver(unittest.TestCase):
    def test_empty_board(self):
        board = Board()
        board.b = [
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ]
        # X goes 1st
        game_is_over = is_game_over(X, board)
        self.assertFalse(game_is_over)

    def test_game_not_over(self):
        board = Board()
        board.b = [
            [O, O, _],
            [X, O, X],
            [X, _, X],
        ]
        x_won = is_game_over(X, board)
        self.assertFalse(x_won)

        board = Board()
        board.b = [
            [O, X, _],
            [_, X, O],
            [X, O, _],
        ]
        o_won = is_game_over(O, board)
        self.assertFalse(o_won)

    def test_X_or_O_wins(self):
        board = Board()
        board.b = [
            [X, X, X],
            [_, O, O],
            [_, _, _],
        ]
        x_won = is_game_over(X, board)
        self.assertTrue(x_won)

        board = Board()
        board.b = [
            [_, O, _],
            [X, O, X],
            [X, O, _],
        ]
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

    def test_detects_win_in_rows(self):
        board = Board()
        board.b = [
            [X, X, X],
            [X, O, _],
            [_, O, O],
        ]
        x_won = is_game_over(X, board)
        self.assertTrue(x_won)

        board = Board()
        board.b = [
            [X, X, O],
            [O, O, O],
            [X, _, X],
        ]
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

        board = Board()
        board.b = [
            [_, X, _],
            [_, X, X],
            [O, O, O],
        ]
        # O just played
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

    def test_detects_win_in_cols(self):
        board = Board()
        board.b = [
            [O, _, X],
            [O, X, X],
            [O, _, _],
        ]
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

        board = Board()
        board.b = [
            [O, X, _],
            [_, X, _],
            [_, X, O],
        ]
        x_won = is_game_over(X, board)
        self.assertTrue(x_won)

        board = Board()
        board.b = [
            [_, _, O],
            [X, X, O],
            [_, X, O],
        ]
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

    def test_detects_win_in_diags(self):
        board = Board()
        board.b = [
            [_, _, X],
            [O, X, O],
            [X, _, _],
        ]
        x_won = is_game_over(X, board)
        self.assertTrue(x_won)

        board = Board()
        board.b = [
            [O, X, _],
            [_, O, X],
            [X, _, O],
        ]
        o_won = is_game_over(O, board)
        self.assertTrue(o_won)

    def test_tied_board_full(self):
        board = Board()
        board.b = [
            [O, X, O],
            [X, O, X],
            [X, O, X],
        ]
        x_won = is_game_over(X, board)
        self.assertIsNone(x_won)

    def test_tied_board_not_full(self):
        board = Board()
        board.b = [
            [X, O, O],
            [O, _, X],
            [X, X, O],
        ]
        # O just played, next move (X's) will result in a tie
        o_won = is_game_over(O, board)
        self.assertIsNone(o_won)

        board = Board()
        board.b = [
            [X, _, O],
            [O, O, X],
            [X, O, X],
        ]
        # O just played, next move (X's) will result in a tie
        o_won = is_game_over(O, board)
        self.assertIsNone(o_won)

if __name__ == "__main__":
    unittest.main()
