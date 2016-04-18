from test_helpers import Helper
from ginmatch import GinMatch
from ginplayer import GinPlayer

class TestGinScore(Helper):

    hand_55_deadwood = [
        (1, 'd'),
        (2, 'c'),
        (3, 'd'),
        (4, 'c'),
        (5, 'c'),
        (6, 'd'),
        (7, 'c'),
        (8, 'd'),
        (9, 'c'),
        (10, 'd'),
    ]

    #Invalid knock just above boundry 11 points of deadwood
    hand_11_deadwood = [
        (1,'d'),
        (2,'h'),
        (3,'h'),
        (4,'h'),
        (5,'h'),
        (6,'h'),
        (7,'h'),
        (8,'h'),
        (9,'h'),
        (10, 'd'),
    ]

    #Valid knock just at 10 points of deadwood
    hand_10_deadwood = [
        (1, 'c'),
        (2, 'c'),
        (3, 'c'),
        (4, 'c'),
        (5, 'c'),
        (6, 'c'),
        (7, 'c'),
        (8, 'c'),
        (9, 'c'),
        (10, 'd'),
    ]

    #Valid knock just above gin 1 points of deadwood
    hand_1_deadwood = [
        (1, 'd'),
        (2, 'c'),
        (3, 'c'),
        (4, 'c'),
        (5, 'c'),
        (6, 'c'),
        (7, 'c'),
        (8, 'c'),
        (9, 'c'),
        (10, 'c'),
    ]

    #Gin (zero points of deadwood)
    hand_0_deadwood = [
        (1, 'c'),
        (2, 'c'),
        (3, 'c'),
        (4, 'c'),
        (5, 'c'),
        (6, 'c'),
        (7, 'c'),
        (8, 'c'),
        (9, 'c'),
        (10, 'c'),
    ]

    #Calculates the score for a normal knock gin to ensure that p1 gets the
    # difference between the deadwood in the hands.
    def test_score_calculation_no_undercut(self):
        gm = self.setup_gin_match(self.hand_1_deadwood, self.hand_11_deadwood)
        self.assertEqual(10, gm.p1_score)
        self.assertEqual(0, gm.p2_score)

    #cacluates score to ensure that the undercut bonus is added to the score
    def test_score_calculation_no_undercut(self):
        gm = self. setup_gin_match(self.hand_1_deadwood, self.hand_0_deadwood)

        self.assertEqual(0, gm.p1_score)
        self.assertEqual(26, gm.p2_score)

    #Calculates score to ensure that gin bonus is added to the score
    def test_score_calculation_gin(self):
        gm = self.setup_gin_match(self.hand_0_deadwood, self.hand_55_deadwood, gin=True)
        self.assertEqual(80, gm.p1_score)
        self.assertEqual(0, gm.p2_score)

    def setup_gin_match(self, hand1, hand2, gin=False):
        p1 = GinPlayer()
        p2 = GinPlayer()
        gm = GinMatch(p1, p2)

        #calculate knock with undercut
        p1hand = self.generate_ginhand_from_card_data(hand1)
        p2hand = self.generate_ginhand_from_card_data(hand2)

        gm.p1.hand = p1hand
        gm.p2.hand = p2hand

        if gin:
            p1.knock_gin(p1hand[0])
        else:
            p1.knock(p1hand[0])

        gm.update_score()
        return gm
