import unittest
from test_helpers import *
from ginhand import *


class TestIsInSet(Helper):

    hand = [
        (1, 'h'), #Not in set
        (2, 'h'), #3 set
        (2, 'c'), #3 set
        (2, 'd'), #3 set
        (3, 'h'), #4 set
        (3, 'c'), #4 set
        (3, 'd'), #4 set
        (3, 's'), #4 set
    ]

    def test_is_in_a_set(self):
        g = self.generate_gincardgroup_from_card_data(self.hand)

        #Test in a set of three
        self.assertFalse(g._is_in_a_3set(GinCard(1, 'h')))
        self.assertTrue(g._is_in_a_3set(GinCard(2, 'h')))
        self.assertFalse(g._is_in_a_3set(GinCard(3, 'c')))

        #Test in a st of four
        self.assertFalse(g._is_in_a_4set(GinCard(1, 'h')))
        self.assertFalse(g._is_in_a_4set(GinCard(2, 'h')))
        self.assertTrue(g._is_in_a_4set(GinCard(3, 'c')))
