import unittest
from gindeck import *

def test_deal_a_card():
    mockDeck = MagicMock()
    mockDeck.deal_a_card.return_value = Card('c', 1)

    gd = GinDeck(mockDeck)
    result = gd.deal_a_card()
    assertEqual(result, GinCard('c', 1))
