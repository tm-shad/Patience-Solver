from enum import Enum
from dataclasses import dataclass


class CardType(Enum):
    number = "N"
    face = "F"


class Color(Enum):
    red = "R"
    black = "B"


class Suit(Enum):
    club = "C"
    spade = "S"
    heart = "H"
    diamond = "D"


class Card:
    def __init__(self):
        pass

    def can_parent(self, *args, **kwargs):
        return True


VALID_NUMBERS = range(6, 11)


@dataclass
class NumberCard(Card):

    color: Color
    number: int

    def can_parent(self, other_card: Card):
        # Will only return true when the other card is:
        #   - A number card
        #   - The opposite color
        #   - Has a value of 1 less than the current card
        return (
            isinstance(other_card, NumberCard)
            and (other_card.color != self.color)
            and (other_card.number == self.number - 1)
        )


@dataclass
class FaceCard(Card):

    suit: Suit

    def can_parent(self, other_card: Card):
        # Will only return true when the other card is:
        #   - A face card
        #   - The same suit
        return isinstance(other_card, FaceCard) and (other_card.suit == self.suit)


def card_from_string(string_rep: str) -> Card:
    """Convert a string into a card object.

    Args:
        string_rep (str): [description]
    """
    card_type = CardType(string_rep[0])

    # case 1: Numbercard
    if card_type == CardType.number:
        color = Color(string_rep[1])
        number = int(string_rep[2:])
        assert number in VALID_NUMBERS
        return NumberCard(color=color, number=number)

    # case 2: Facecard
    if card_type == CardType.face:
        suit = Suit(string_rep[1])
        return FaceCard(suit=suit)
