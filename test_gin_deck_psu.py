import unittest
from gindeck import *

def test_deal_a_card():
    mockDeck = MagicMock()
    mockDeck.deal_a_card.return_value = Card(2, 'c')
    mockDeck.deal_a_card.return_value = Card(11, 'd')

    #Test that we get the top card back from the mock
    gd = GinDeck(mockDeck)
    result = gd.deal_a_card()
    assertEqual(result, GinCard(2, 'c'))
    assertEqual(result.point_value, 2)

    #Test that the Gin Card returns the proper value
    result = gd.deal_a_card()
    assertEqual(result.point_value, 10)
