import patience_solver.game_rules.cards as cards
import pytest


def test_card_from_string():
    # check valid face card
    assert cards.card_from_string("FC-") == cards.FaceCard(cards.Suit.club)

    # chack valid number cards
    assert cards.card_from_string("NR6") == cards.NumberCard(cards.Color.red, 6)
    assert cards.card_from_string("NB10") == cards.NumberCard(cards.Color.black, 10)

    # check invalid string
    with pytest.raises(ValueError):
        cards.card_from_string("NB")
    with pytest.raises(IndexError):
        pytest.raises(cards.card_from_string(""))
    with pytest.raises(ValueError):
        pytest.raises(cards.card_from_string("aaaaaa"))
