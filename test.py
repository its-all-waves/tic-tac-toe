import unittest
from main import Board, X, O

_ = None


class TestIsGameOver(unittest.TestCase):
    def assert_game_state_is(
        self, result: Board.GameState, expected: Board.GameState
    ):
        self.assertEqual(result, expected)

    def test_empty_board(self):
        board = Board()
        board._b = [
            [_, _, _],
            [_, _, _],
            [_, _, _],
        ]
        # X goes 1st
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "GAME_IN_PROGRESS")

    def test_game_not_over(self):
        board = Board()
        board._b = [
            [O, O, _],
            [X, O, X],
            [X, _, X],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "GAME_IN_PROGRESS")

        board = Board()
        board._b = [
            [O, X, _],
            [_, X, O],
            [X, O, _],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "GAME_IN_PROGRESS")

    def test_X_or_O_wins(self):
        board = Board()
        board._b = [
            [X, X, X],
            [_, O, O],
            [_, _, _],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [_, O, _],
            [X, O, X],
            [X, O, _],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

    def test_detects_win_in_rows(self):
        board = Board()
        board._b = [
            [X, X, X],
            [X, O, _],
            [_, O, O],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [X, X, O],
            [O, O, O],
            [X, _, X],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [_, X, _],
            [_, X, X],
            [O, O, O],
        ]
        # O just played
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

    def test_detects_win_in_cols(self):
        board = Board()
        board._b = [
            [O, _, X],
            [O, X, X],
            [O, _, _],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [O, X, _],
            [_, X, _],
            [_, X, O],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [_, _, O],
            [X, X, O],
            [_, X, O],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

    def test_detects_win_in_diags(self):
        board = Board()
        board._b = [
            [_, _, X],
            [O, X, O],
            [X, _, _],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

        board = Board()
        board._b = [
            [O, X, _],
            [_, O, X],
            [X, _, O],
        ]
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "PLAYER_IS_WINNER")

    def test_tied_board_full(self):
        board = Board()
        board._b = [
            [O, X, O],
            [X, O, X],
            [X, O, X],
        ]
        state = board.is_game_over(X)
        self.assert_game_state_is(state, "TIE")

    def test_tied_board_not_full(self):
        board = Board()
        board._b = [
            [X, O, O],
            [O, _, X],
            [X, X, O],
        ]
        # O just played, next move (X's) will result in a tie
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "TIE")

        board = Board()
        board._b = [
            [X, _, O],
            [O, O, X],
            [X, O, X],
        ]
        # O just played, next move (X's) will result in a tie
        state = board.is_game_over(O)
        self.assert_game_state_is(state, "TIE")


if __name__ == "__main__":
    unittest.main()
