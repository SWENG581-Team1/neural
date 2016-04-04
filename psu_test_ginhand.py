import unittest
import random

from deck import *
from ginhand import *
from psu_test_helper import *

# noinspection PyProtectedMember
class PSUTestGinHand(unittest.TestCase):
    
    ec_hand_data1 = [
        (2, 'h'),
        (3, 'c'),
        (4, 's'),
        (5, 's'),
        (6, 's'),
        (7, 's'),
        (8, 's'),
        (9, 'c'),
        (10, 'h'),
        (11, 'c'),
    ]

    ec_hand_data2 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (2, 'd'),
        (3, 's'),
        (4, 's'),
        (5, 's'),
        (6, 's'),
        (7, 'c'),
        (8, 'h')
    ]

    ec_hand_data3 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (10, 'h'),
        (10, 'c'),
        (10, 's'),
        (5, 's'),
        (6, 's'),
        (7, 'c'),
        (8, 'h')
    ]

    ec_hand_data4 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (10, 'h'),
        (10, 'c'),
        (10, 's'),
        (11, 'h'),
        (11, 'c'),
        (11, 's'),
        (8, 'h')
    ]

    ec_hand_data5 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (3, 's'),
        (4, 's'),
        (5, 's'),
        (6, 's'),
        (7, 'c'),
        (8, 'h')
    ]

    ec_hand_data6 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (10, 'h'),
        (10, 'c'),
        (10, 's'),
        (10, 'd'),
        (7, 'c'),
        (8, 'h')
    ]

    ec_hand_data7 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (10, 'h'),
        (10, 'c'),
        (10, 's'),
        (1, 's'),
        (2, 'c'),
        (3, 'h')
    ]

    ec_hand_data8 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (3, 'h'),
        (3, 'c'),
        (3, 's'),
        (4, 'h'),
        (4, 'c'),
        (4, 's')
    ]
    
    def setUp(self):
        pass
    
    @staticmethod
    def generate_ginhand_from_card_data(cdata):
        g = GinHand()
        for c in cdata:
            g.add_card(GinCard(c[0], c[1]))
        return g
    
    # Random testing of GinHand.is_in_a_3set
    def test_enumerate_all_sets(self):        
        ec1_hand = self.generate_ginhand_from_card_data(self.ec_hand_data1)
        result = ec1_hand.enumerate_all_sets()
        assert (result.__len__() == 0)
        
        ec2_hand = self.generate_ginhand_from_card_data(self.ec_hand_data2)
        result = ec2_hand.enumerate_all_sets()
        assert (result.__len__() == 1)
        
        ec3_hand = self.generate_ginhand_from_card_data(self.ec_hand_data3)
        result = ec3_hand.enumerate_all_sets()
        assert (result.__len__() == 2)
        
        ec4_hand = self.generate_ginhand_from_card_data(self.ec_hand_data4)
        result = ec4_hand.enumerate_all_sets()
        assert (result.__len__() == 3)
        
        ec5_hand = self.generate_ginhand_from_card_data(self.ec_hand_data5)
        result = ec5_hand.enumerate_all_sets()
        assert (result.__len__() == 5)
        
        ec6_hand = self.generate_ginhand_from_card_data(self.ec_hand_data6)
        result = ec6_hand.enumerate_all_sets()
        assert (result.__len__() == 10)
        
        ec7_hand = self.generate_ginhand_from_card_data(self.ec_hand_data7)
        result = ec7_hand.enumerate_all_sets()
        assert (result.__len__() == 6)
        
        ec8_hand = self.generate_ginhand_from_card_data(self.ec_hand_data8)
        result = ec8_hand.enumerate_all_sets()
        assert (result.__len__() == 7)
        
if __name__ == '__main__':
    unittest.main()