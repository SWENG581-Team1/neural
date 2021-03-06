
from deck import *
import unittest
from operator import attrgetter


class TestCard(unittest.TestCase):

    def test_new_card(self):
        c = Card(1, 'c')

        self.assertEqual(c.rank, 1)
        self.assertEqual(c.suit, 'c')

    def test_sanity(self):
        with self.assertRaises(AttributeError):
            Card(10, 'x')

        with self.assertRaises(AttributeError):
            Card(100, 'c')

    def test___cmp__(self):
        card1 = Card(6, 'c')
        card2 = Card(5, 'd')
        card3 = Card(6, 's')

        self.assertLessEqual(card1.__cmp__(card2), -1)
        self.assertLessEqual(card1.__cmp__(card3), -1)
        self.assertEqual(card1.__cmp__(card1), 0)

        self.assertGreaterEqual(card2.__cmp__(card1), 1)
        self.assertLessEqual(card2.__cmp__(card3), -1)

        self.assertGreaterEqual(card3.__cmp__(card1), 1)
        self.assertGreaterEqual(card3.__cmp__(card2), 1)

    def test_to_s(self):
        c = Card(9, 'c')
        self.assertEqual('9c', c.to_s())

    def test_ranking(self):
        # sort the deck and ensure that each card returns its proper ranking.
        d = Deck()
        d.cards.sort(key=lambda c: (c.suit, c.rank))
        for i in range(51):
            self.assertEqual(d.cards[i].ranking(), i+1)


class TestDeck(unittest.TestCase):
    def test_new_deck(self):
        d = Deck()
        self.assertEqual(len(d.cards), 52)

    def test_shuffle(self):
        d = Deck()
        d.cards.sort(key=attrgetter('rank', 'suit'))
        before = list(d.cards)
        d.shuffle()
        self.assertNotEqual(before, d.cards)

    def test_deal_a_card(self):
        d = Deck()
        topcard = d.cards[51]
        c = d.deal_a_card()
        self.assertEqual(51, len(d.cards))
        self.assertEqual(topcard, c)
