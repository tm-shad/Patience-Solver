from dataclasses import dataclass
from os import linesep
from typing import List
from patience_solver.game_rules.cards import (
    CardType,
    Card,
    FaceCard,
    NumberCard,
    card_from_string,
)

import patience_solver.game_rules.cards as game_cards

from collections import defaultdict

from pathlib import Path

TOTAL_GAMEBOARD_COLS = 9
TOTAL_GAMEBOARD_FREE_CELLS = 1


@dataclass
class Column:
    cards: List[Card]

    @classmethod
    def from_string(cls, card_strings: str):
        cards = (
            [card_from_string(i) for i in card_strings.split(" ")]
            if len(card_strings)
            else []
        )

        return Column(cards=cards)

    def __len__(self):
        return len(self.cards)

    def valid_transfer_from(self, other_col):
        # check if my tail card can parent the other columns tail card

        return self.tail().can_parent(other_col.tail())

    def tail(self) -> Card:
        return (
            self.cards[-1] if len(self.cards) else Card()
        )  # return the final card in the list, if the list is empty then return the root card

    def pop(self):
        return self.cards.pop()

    def push(self, new_card: Card):
        assert self.tail().can_parent(new_card)

        self.cards.append(new_card)

    def is_complete(self):
        return False  # TODO: check if the column can be considered complete


@dataclass
class FreeSpace(Column):
    cards: List[Card]

    @classmethod
    def from_string(cls, card_strings: str):
        cards = (
            [card_from_string(i) for i in card_strings.split(" ")]
            if len(card_strings)
            else []
        )

        assert len(cards) <= 1  # since the free space can only hold a single card
        return FreeSpace(cards=cards)

    def valid_transfer_from(self, other_col):
        # check if my tail card can parent the other columns tail card

        return (len(self.cards) == 0) and (self.tail().can_parent(other_col.tail()))

    def push(self, new_card: Card):
        assert self.tail().can_parent(new_card)
        assert len(self.cards) == 0

        self.cards.append(new_card)

    def is_complete(self):
        return False  # len(self.cards) == 0  # this columns is only complete when it is empty


@dataclass
class GameBoard:
    columns: List[Column]

    @classmethod
    def from_text_file(cls, text_file: Path):
        with text_file.open() as f:
            raw_text = f.read()
        lines = raw_text.split("\n")

        assert len(lines) == TOTAL_GAMEBOARD_COLS + TOTAL_GAMEBOARD_FREE_CELLS

        # create normal columns
        columns = []

        for i in range(0, TOTAL_GAMEBOARD_COLS):
            columns.append(Column.from_string(lines[i]))

        # create free space
        for i in range(
            TOTAL_GAMEBOARD_COLS, TOTAL_GAMEBOARD_COLS + TOTAL_GAMEBOARD_FREE_CELLS
        ):
            columns.append(FreeSpace.from_string(lines[i]))

        # Validate that a correct board was made
        ret_board = GameBoard(columns=columns)

        ret_board.validate_board()

        return ret_board

    def validate_board(self):
        card_counts = defaultdict(lambda: 0)
        for col in self.columns:
            for card in col.cards:
                if isinstance(card, FaceCard):
                    card_counts[(CardType.face, card.suit)] += 1
                else:
                    card_counts[(CardType.number, card.color, card.number)] += 1

        # there should be exactly 4 of each face card
        for suit in game_cards.Suit:
            assert card_counts[(CardType.face, suit)] == 4

        # there should be exactly 2 of each color/number pair
        for color in game_cards.Color:
            for number in game_cards.VALID_NUMBERS:
                card_counts[(CardType.number, color, number)] == 2

        # there should be a specific number of total cards, no more no less
        expected_total = 4 * len(game_cards.Suit) + 2 * len(
            game_cards.VALID_NUMBERS
        ) * len(game_cards.Color)
        assert sum(card_counts.values()) == expected_total

    def check_move(self, col1: int, col2: int):
        return self.columns[col2].valid_transfer_from(self.columns[col1])

    def make_move(self, col1: int, col2: int):
        self.columns[col2].push(self.columns[col1].pop())
        self.validate_board()

    def completed_cols(self) -> List[bool]:
        return [col.is_complete() for col in self.columns]
