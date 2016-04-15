import unittest
from gintable import GinTable
from gintable import TableSeatingError
from ginplayer import GinPlayer

class TestSeatPlayer(unittest.TestCase):
    def test_seat_player(self):
        gt = GinTable()
        gp1 = GinPlayer()
        gp2 = GinPlayer()
        #try to seat 1 player
        self.assertTrue(gt.seat_player(gp1))

        #try to seat the same player twice
        with self.assertRaises(TableSeatingError):
            gt.seat_player(gp1)

        #try to seat a 2 player
        self.assertTrue(gt.seat_player(gp2))

        with self.assertRaises(TableSeatingError):
            gt.seat_player(GinPlayer())
