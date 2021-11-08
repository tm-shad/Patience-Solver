import patience_solver.game_rules.gameboard as gameboard
import patience_solver.game_rules.cards as cards
import pytest

from pathlib import Path


class TestColumn:
    def test_from_string(self):
        # Test valid string
        assert gameboard.Column.from_string("NR6 NR5 NR4") == gameboard.Column(
            cards=[
                cards.NumberCard(color=cards.Color.red, number=6),
                cards.NumberCard(color=cards.Color.red, number=5),
                cards.NumberCard(color=cards.Color.red, number=4),
            ]
        )

        # Test valid empty string
        assert gameboard.Column.from_string("") == gameboard.Column(cards=[])

        # Test invalid strings
        with pytest.raises(ValueError):
            gameboard.Column.from_string("abcdefg")


class TestFreeSpace:
    def test_from_string(self):
        # Test valid string
        gameboard.FreeSpace.from_string("NR6") == gameboard.FreeSpace(
            cards=[
                cards.NumberCard(color=cards.Color.red, number=6),
            ]
        )
        # Test valid empty string
        gameboard.FreeSpace.from_string("") == gameboard.FreeSpace(cards=[])

        # Test invalid string
        with pytest.raises(AssertionError):
            gameboard.FreeSpace.from_string("NR6 NR5")


class TestGameBoard:
    def test_from_text_file(self, test_board_1_text):
        gameboard.GameBoard.from_text_file(test_board_1_text)

    def test_check_move(self, test_board_1_text):
        gb = gameboard.GameBoard.from_text_file(test_board_1_text)

        assert gb.check_move(0, 9) is True
        assert gb.check_move(0, 1) is False

    def test_make_move(self, test_board_1_text):
        gb = gameboard.GameBoard.from_text_file(test_board_1_text)

        # try a valid move
        col1, col2 = 0, 9
        original_lengths = (len(gb.columns[col1]), len(gb.columns[col2]))
        gb.make_move(col1, col2)
        assert len(gb.columns[col1]) == original_lengths[0] - 1
        assert len(gb.columns[col2]) == original_lengths[1] + 1

        # try invalid move
        col1, col2 = 0, 8
        original_lengths = (len(gb.columns[col1]), len(gb.columns[col2]))
        with pytest.raises(AssertionError):
            gb.make_move(col1, col2)
