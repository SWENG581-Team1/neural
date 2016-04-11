import random
from test_helpers import *
from ginhand import *


# noinspection PyProtectedMember,PyMethodMayBeStatic
class TestGinCardGroup(Helper):
    maxDiff = None

    def test___repr__(self):
        card_list = [GinCard(1, 'c'), GinCard(2, 'd'), GinCard(3, 's')]
        gcg = GinCardGroup(card_list)

        self.assertEqual("1c 2d 3s", gcg.__repr__())

    def test___cmp_(self):
        card_group_first  = GinCardGroup([GinCard(1, 'c'), GinCard(2, 'c'), GinCard(3, 'c')])
        card_group_second = GinCardGroup([GinCard(1, 'c'), GinCard(1, 'd'), GinCard(1, 'h')])
        card_group_third  = GinCardGroup([GinCard(2, 'c'), GinCard(3, 'c'), GinCard(4, 'c')])
        card_group_fourth = GinCardGroup([GinCard(2, 'c'), GinCard(3, 'c'), GinCard(4, 'c'), GinCard(5, 'c')])

        # test equality
        self.assertEqual(card_group_first.__cmp__(card_group_first), 0)

        # test less than
        self.assertLessEqual(card_group_first.__cmp__(card_group_second), -1)
        self.assertLessEqual(card_group_first.__cmp__(card_group_third), -1)
        self.assertLessEqual(card_group_first.__cmp__(card_group_fourth), -1)
        self.assertLessEqual(card_group_second.__cmp__(card_group_third), -1)
        self.assertLessEqual(card_group_second.__cmp__(card_group_fourth), -1)
        self.assertLessEqual(card_group_third.__cmp__(card_group_fourth), -1)

        # test greater than
        self.assertGreaterEqual(card_group_second.__cmp__(card_group_first), 1)
        self.assertGreaterEqual(card_group_third.__cmp__(card_group_first),  1)
        self.assertGreaterEqual(card_group_third.__cmp__(card_group_second), 1)
        self.assertGreaterEqual(card_group_fourth.__cmp__(card_group_first), 1)
        self.assertGreaterEqual(card_group_fourth.__cmp__(card_group_second), 1)
        self.assertGreaterEqual(card_group_fourth.__cmp__(card_group_third), 1)

    def test_iterable(self):
        gcg_catcher = GinCardGroup()
        gcg_control = self.generate_gincardgroup_from_card_data(self.card_data1)
        for c in gcg_control:
            gcg_catcher.add_card(c)

        self.assertEqual(10, gcg_catcher.size())

        # verify that catcher matches card_data1 card-by-card (rank/suit as well as order)
        for index in range(9):
            card = Card(gcg_control.cards[index].rank, gcg_control.cards[index].suit)
            self.assertEqual(0, gcg_catcher.cards[index].__cmp__(card))

    def test_new_gincardgroup(self):
        cg = self.generate_gincardgroup_from_card_data(self.card_data1)

        self.assertEqual(10, len(cg.cards))

    def test_new_gincardgroup_empty(self):
        cg = GinCardGroup()
        self.assertEqual(0, len(cg.cards))

    def test_add_card(self):
        cg = GinCardGroup()
        c = GinCard(7, 'h')
        cg.add_card(c)
        self.assertEqual(1, len(cg.cards))
        self.assertEqual(7, cg.cards[0].rank)
        self.assertEqual('h', cg.cards[0].suit)

        next_card = GinCard(4, 'd')
        cg.add_card(next_card)
        self.assertEqual(next_card, cg.cards[0])

        next_card = GinCard(8, 'd')
        cg.add_card(next_card)
        self.assertEqual(next_card, cg.cards[1])

        next_card = GinCard(10, 'h')
        cg.add_card(next_card)
        self.assertEqual(next_card, cg.cards[3])

    def test_discard(self):
        g = GinCardGroup()
        gc = GinCard(5, 'c')
        g.add_card(gc)
        self.assertEqual(1, g.size())
        g.discard(gc)
        self.assertEqual(0, g.size())

    def test_discard_not_holding_said_card(self):
        g = GinCardGroup()
        gc_yes = GinCard(5, 'c')
        gc_no = GinCard(7, 'd')
        g.add_card(gc_yes)
        self.assertEqual(1, g.size())
        g.discard(gc_no)
        self.assertEqual(1, g.size())

    # make sure we handle discarding properly when we have an empty hand
    def test_discard_empty_hand(self):
        g = GinCardGroup()
        gc = GinCard(5, 'c')
        g.discard(gc)
        self.assertEqual(0, g.size())

    def test_sort(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data1)
        # the add_card function sorts after each add. randomize here to bypass it.
        random.shuffle(g.cards)

        g.sort()
        # 5c should be first
        self.assertEqual(5, g.cards[0].rank)
        self.assertEqual('c', g.cards[0].suit)
        # 9c should be second
        self.assertEqual(9, g.cards[1].rank)
        self.assertEqual('c', g.cards[1].suit)
        # Kc should be third
        self.assertEqual(9, g.cards[2].rank)
        self.assertEqual('h', g.cards[2].suit)
        # Ks should be fourth
        self.assertEqual(9, g.cards[3].rank)
        self.assertEqual('s', g.cards[3].suit)
        # 5c should be fifth
        self.assertEqual(10, g.cards[4].rank)
        self.assertEqual('s', g.cards[4].suit)
        # 9c should be sixth
        self.assertEqual(11, g.cards[5].rank)
        self.assertEqual('s', g.cards[5].suit)
        # Kc should be seventh
        self.assertEqual(12, g.cards[6].rank)
        self.assertEqual('s', g.cards[6].suit)
        # Ks should be eighth
        self.assertEqual(13, g.cards[7].rank)
        self.assertEqual('c', g.cards[7].suit)
        # Kc should be ninth
        self.assertEqual(13, g.cards[8].rank)
        self.assertEqual('h', g.cards[8].suit)
        # Ks should be tenth and final card
        self.assertEqual(13, g.cards[-1].rank)
        self.assertEqual('s', g.cards[-1].suit)

    def test_sort_by_suit(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data1)
        random.shuffle(g.cards)

        g.sort(by_suit=True)
        # 5c should be first
        self.assertEqual(5, g.cards[0].rank)
        self.assertEqual('c', g.cards[0].suit)
        # 9c should be second
        self.assertEqual(9, g.cards[1].rank)
        self.assertEqual('c', g.cards[1].suit)
        # Kc should be third
        self.assertEqual(13, g.cards[2].rank)
        self.assertEqual('c', g.cards[2].suit)
        # 9h should be fourth
        self.assertEqual(9, g.cards[3].rank)
        self.assertEqual('h', g.cards[3].suit)
        # Kh should be fifth
        self.assertEqual(13, g.cards[4].rank)
        self.assertEqual('h', g.cards[4].suit)
        # 9s should be sixth
        self.assertEqual(9, g.cards[5].rank)
        self.assertEqual('s', g.cards[5].suit)
        # 10c should be seventh
        self.assertEqual(10, g.cards[6].rank)
        self.assertEqual('s', g.cards[6].suit)
        # Js should be eighth
        self.assertEqual(11, g.cards[7].rank)
        self.assertEqual('s', g.cards[7].suit)
        # Qs should be ninth
        self.assertEqual(12, g.cards[8].rank)
        self.assertEqual('s', g.cards[8].suit)
        # Ks should be tenth and final card
        self.assertEqual(13, g.cards[-1].rank)
        self.assertEqual('s', g.cards[-1].suit)

    def test_size(self):
        cg = GinCardGroup()
        self.assertEqual(0, cg.size())
        cg.add_card(GinCard(2, 'd'))
        self.assertEqual(1, cg.size())

    def test_contains(self):
        cg = self.generate_gincardgroup_from_card_data(self.card_data1)
        self.assertEqual(True, cg.contains(5, 'c'))
        self.assertEqual(False, cg.contains(5, 'd'))

    def test_contains_card(self):
        cg = self.generate_gincardgroup_from_card_data(self.card_data1)
        card_yes = GinCard(5, 'c')
        card_no  = GinCard(5, 'd')

        self.assertEqual(True, cg.contains_card(card_yes))
        self.assertEqual(False, cg.contains_card(card_no))

    def test_points(self):
        # build and test a small hand
        cg1 = GinCardGroup()
        self.assertEqual(0, cg1.points())

        cg1.add_card(GinCard(9, 'c'))
        self.assertEqual(9, cg1.points())

        cg1.add_card(GinCard(11, 'c'))
        self.assertEqual(19, cg1.points())

        # test something bigger
        cg2 = self.generate_gincardgroup_from_card_data(self.card_data1)
        self.assertEqual(92, cg2.points())

    def test_sum_points_zero(self):
        cg = GinCardGroup()
        self.assertEqual(0, cg.points())

    def build_meldgroup_list_from_data(self, expected_melds_data):
        expected_melds_gcg = []
        for row in expected_melds_data:
            gcg = GinCardGroup()
            for card in row:
                gcg.add_card(GinCard(card[0], card[1]))
            expected_melds_gcg.append(gcg)
        return expected_melds_gcg

    def test_enumerate_all_melds_and_sets(self):
        expected_melds_data = [[(9,  'c'), (9,  'h'), (9,  's')],
                                [(9,  's'), (10, 's'), (11, 's')],
                                [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                                [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                                [(10, 's'), (11, 's'), (12, 's')],
                                [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                                [(11, 's'), (12, 's'), (13, 's')],
                                [(13, 'c'), (13, 'h'), (13, 's')],
                               ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        g = self.generate_gincardgroup_from_card_data(self.card_data1)
        generated_melds = g.enumerate_all_melds_and_sets()

        self.compare_arrays_of_cardgroups(GinCardGroup.sort_melds(expected_melds), generated_melds)

    def test_enumerate_all_melds_and_sets_quads(self):
        expected_melds_data = [[(9,  'c'), (9,  'd'), (9,  'h')],
                          [(9,  'c'), (9,  'd'), (9,  'h'), (9, 's')],
                          [(9,  'c'), (9,  'd'), (9,  's')],
                          [(9,  'c'), (9,  'h'), (9,  's')],
                          [(9,  'd'), (9,  'h'), (9,  's')],
                          [(9,  's'), (10, 's'), (11, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(10, 's'), (11, 's'), (12, 's')],
                          [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(11, 's'), (12, 's'), (13, 's')],
                          [(13, 'c'), (13, 'h'), (13, 's')],
                          ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        g = self.generate_gincardgroup_from_card_data(self.card_data2)
        generated_melds = g.enumerate_all_melds_and_sets()

        self.compare_arrays_of_cardgroups(expected_melds, generated_melds)

    def test_enumerate_all_melds(self):
        expected_melds_data = [[(9,  's'), (10, 's'), (11, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(10, 's'), (11, 's'), (12, 's')],
                          [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(11, 's'), (12, 's'), (13, 's')],
                          ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        g = self.generate_gincardgroup_from_card_data(self.card_data2)
        generated_melds = g.enumerate_all_melds()

        self.compare_arrays_of_cardgroups(expected_melds, generated_melds)

    def test_enumerate_all_sets(self):
        expected_melds_data = [[(9,  'c'), (9,  'd'), (9,  'h')],
                          [(9,  'c'), (9,  'd'), (9, 'h'), (9, 's')],
                          [(9,  'c'), (9,  'd'), (9,  's')],
                          [(9,  'c'), (9,  'h'), (9,  's')],
                          [(9,  'd'), (9,  'h'), (9,  's')],
                          [(13, 'c'), (13, 'h'), (13, 's')],
                          ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        g = self.generate_gincardgroup_from_card_data(self.card_data2)
        generated_melds = g.enumerate_all_sets()

        self.compare_arrays_of_cardgroups(expected_melds, generated_melds)

    def test__is_in_a_meld(self):
        cgroup = self.generate_gincardgroup_from_card_data(self.card_data1)

        # all cards in card_data1 except for the 5c,9h,9c,Kc,Kh should be marked as being in a meld
        for c in self.card_data1:
            gc = GinCard(c[0], c[1])
            if (c[0] == 5 and c[1] == 'c') or (
                    c[0] == 9  and c[1] == 'c') or (
                    c[0] == 9  and c[1] == 'h') or (
                    c[0] == 13 and c[1] == 'c') or (
                    c[0] == 13 and c[1] == 'h'):
                self.assertEqual(False, cgroup._is_in_a_meld(gc), "F-rank: %d, suit: %s" % (gc.rank, gc.suit))
            else:
                self.assertEqual(True, cgroup._is_in_a_meld(gc), "T-rank: %d, suit: %s" % (gc.rank, gc.suit))

    def test__is_in_a_meld_branch_coverage(self):
        #card group 7 only has 2 cards
        cgroup = self.generate_gincardgroup_from_card_data(self.card_data7)
        for c in self.card_data7:
            card = GinCard(c[0], c[1])
            self.assertEqual(False, cgroup._is_in_a_meld(card), "Failed to detect undersized hand")

        cgroup = self.generate_gincardgroup_from_card_data(self.card_data8)
        for c in self.card_data8:
            card = GinCard(c[0], c[1])
            self.assertEqual(False, cgroup._is_in_a_meld(card), "F-rank: %d, suit: %s" % (card.rank, card.suit))

        cgroup = self.generate_gincardgroup_from_card_data(self.card_data9)
        for c in self.card_data9:
            card = GinCard(c[0], c[1])
            self.assertEqual(True, cgroup._is_in_a_meld(card), "T-rank: %d, suit: %s" % (card.rank, card.suit))

    def test__is_in_a_3set(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data2)

        self.assertEqual(False, g._is_in_a_3set(GinCard(9, 's')))
        self.assertEqual(False, g._is_in_a_3set(GinCard(10, 's')))
        self.assertEqual(True, g._is_in_a_3set(GinCard(13, 's')))

        # test a card not in the hand
        self.assertEqual(False, g._is_in_a_3set(GinCard(1, 's')))

    def test__is_in_a_4set(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data2)
        gc_yes = GinCard(9, 'c')
        gc_no = GinCard(10, 'c')

        self.assertEqual(True, g._is_in_a_4set(gc_yes))
        self.assertEqual(False, g._is_in_a_4set(gc_no))

        # test a card not in the hand
        self.assertEqual(False, g._is_in_a_4set(GinCard(1, 'c')))

    def test_sort_melds__only_melds(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data2)

        expected_melds_data = [[(9,  's'), (10, 's'), (11, 's')],
                                [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                                [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                                [(10, 's'), (11, 's'), (12, 's')],
                                [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                                [(11, 's'), (12, 's'), (13, 's')],
                               ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        test_melds = g.enumerate_all_melds()
        shuffle(test_melds)

        sorted_melds = GinCardGroup.sort_melds(test_melds)

        self.compare_arrays_of_cardgroups(expected_melds, sorted_melds)

    def test_sort_melds__melds_and_sets(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data2)

        expected_melds_data = [[(9,  'c'), (9,  'd'), (9,  'h')],
                          [(9,  'c'), (9,  'd'), (9,  'h'), (9, 's')],
                          [(9,  'c'), (9,  'd'), (9,  's')],
                          [(9,  'c'), (9,  'h'), (9,  's')],
                          [(9,  'd'), (9,  'h'), (9,  's')],
                          [(9,  's'), (10, 's'), (11, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(10, 's'), (11, 's'), (12, 's')],
                          [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(11, 's'), (12, 's'), (13, 's')],
                          [(13, 'c'), (13, 'h'), (13, 's')],
                          ]

        expected_melds = self.build_meldgroup_list_from_data(expected_melds_data)

        test_melds = g.enumerate_all_melds_and_sets()
        shuffle(test_melds)

        sorted_melds = GinCardGroup.sort_melds(test_melds)

        self.compare_arrays_of_cardgroups(expected_melds, sorted_melds)

    def test_uniqsort_cardgroups(self):
        # starting with an unsorted aGCG with a duplicate AND a GCG with an out-of-order cards array
        agcg = [GinCardGroup([GinCard(1, 'c'), GinCard(2, 'c'), GinCard(3, 'c')]),
                GinCardGroup([GinCard(2, 'd'), GinCard(2, 'c'), GinCard(2, 'h')]),
                GinCardGroup([GinCard(1, 'c'), GinCard(2, 'c'), GinCard(3, 'c')])]

        cleaned = GinCardGroup.uniqsort_cardgroups(agcg)

        # ensure we dedupe
        self.assertEqual(2, len(cleaned))

        # ensure we sort
        self.assertEqual(cleaned[0].__repr__(), "1c 2c 3c")
        self.assertEqual(cleaned[1].__repr__(), "2c 2d 2h")

    def test_get_card_at_index(self):
        g = self.generate_gincardgroup_from_card_data(self.card_data1)

        target = g.get_card_at_index(0)
        self.assertEqual(target, g.cards[0])

    def test_deadwood_cards(self):
        # something simple
        gh = self.generate_gincardgroup_from_card_data(self.card_data1)

        self.assertIsInstance(gh.deadwood_cards(), GinCardGroup)
        self.assertEqual(1, gh.deadwood_cards().size())
        self.assertTrue(gh.deadwood_cards().contains(5, 'c'))

        # something bigger
        gh = self.generate_gincardgroup_from_card_data(self.card_data5)

        self.assertIsInstance(gh.deadwood_cards(), GinCardGroup)
        self.assertEqual(7, gh.deadwood_cards().size())

    def test__prune_meld_group(self):
        a = GinCardGroup([GinCard(9, 'c'), GinCard(10, 'c'), GinCard(11, 'c')])
        b = GinCardGroup([GinCard(9, 'c'), GinCard(9,  'h'), GinCard(9,  's')])
        c = GinCardGroup([GinCard(1, 'c'), GinCard(2,  'c'), GinCard(3,  'c')])
        p = GinCardGroup([GinCard(9, 'c')])
        melds = [a, b, c]

        pruned = GinCardGroup._prune_meld_group(melds, p)
        self.assertEqual(1, len(pruned))

        # something bigger
        pruner_meld = GinCardGroup([GinCard(9, 'c'), GinCard(10, 'c'), GinCard(11, 'c')])

        meld_data = [[(9,  'c'), (9,  'd'), (9,  'h')],
                          [(9,  'c'), (9,  'd'), (9,  'h'), (9, 's')],
                          [(9,  'c'), (9,  'd'), (9,  's')],
                          [(9,  'c'), (9,  'h'), (9,  's')],
                          [(9,  'd'), (9,  'h'), (9,  's')],
                          [(9,  's'), (10, 's'), (11, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's')],
                          [(9,  's'), (10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(10, 's'), (11, 's'), (12, 's')],
                          [(10, 's'), (11, 's'), (12, 's'), (13, 's')],
                          [(11, 's'), (12, 's'), (13, 's')],
                          [(13, 'c'), (13, 'h'), (13, 's')]
                         ]

        melds = []
        for data_row in meld_data:
            card_list = []
            for data in data_row:
                card_list.append(GinCard(data[0], data[1]))
            melds.append(GinCardGroup(card_list))

        cleaned = GinCardGroup._prune_meld_group(melds, pruner_meld)

        self.assertEqual(8, len(cleaned))

    def test__prune_meld_group_empty_pruner(self):
        a = GinCardGroup([GinCard(9, 'c'), GinCard(10, 'c'), GinCard(11, 'c')])
        b = GinCardGroup([GinCard(9, 'c'), GinCard(9,  'h'), GinCard(9,  's')])
        c = GinCardGroup([GinCard(1, 'c'), GinCard(2,  'c'), GinCard(3,  'c')])
        p = GinCardGroup()
        melds = [a, b, c]

        pruned = GinCardGroup._prune_meld_group(melds, p)
        self.assertEqual(3, len(pruned))

    def test_deadwood_count(self):
        g1 = self.generate_ginhand_from_card_data(self.card_data1)
        self.assertEqual(5, g1.deadwood_count())

        g2 = self.generate_ginhand_from_card_data(self.card_data2)
        self.assertEqual(0, g2.deadwood_count())

        g4 = self.generate_ginhand_from_card_data(self.card_data4)
        self.assertEqual(26, g4.deadwood_count())

    def test__examine_melds(self):
        # empty hand = 0 deadwood
        empty_hand = GinCardGroup()
        self.assertEqual(0, empty_hand._examine_melds(empty_hand))

        # 1c,2d hand = 3 deadwood
        two_card_hand = GinCardGroup()
        two_card_hand.add_card(GinCard(1, 'c'))
        two_card_hand.add_card(GinCard(2, 'd'))
        self.assertEqual(3, two_card_hand._examine_melds(two_card_hand))

        # 1c,2d,3h hand = 6 deadwood
        three_card_hand = GinCardGroup()
        three_card_hand.add_card(GinCard(1, 'c'))
        three_card_hand.add_card(GinCard(2, 'd'))
        three_card_hand.add_card(GinCard(3, 'h'))
        self.assertEqual(6, three_card_hand._examine_melds(three_card_hand))

        # 1c,2d,3h,4h,5h hand = 3 deadwood
        five_card_hand = GinCardGroup()
        five_card_hand.add_card(GinCard(1, 'c'))
        five_card_hand.add_card(GinCard(2, 'd'))
        five_card_hand.add_card(GinCard(3, 'h'))
        five_card_hand.add_card(GinCard(4, 'h'))
        five_card_hand.add_card(GinCard(5, 'h'))
        self.assertEqual(3, five_card_hand._examine_melds(five_card_hand))

        g = self.generate_ginhand_from_card_data(self.card_data1)
        self.assertEqual(5, g._examine_melds(g))


# noinspection PyProtectedMember
class TestGinHand(Helper):
    maxDiff = None

    def testNewGinHand(self):
        g = GinHand()
        self.assertEqual(0, g.size())

    def test_process_layoff_single_set(self):
        gh_layer = self.generate_ginhand_from_card_data(self.card_data1)
        gh_winner = self.generate_ginhand_from_card_data(self.card_data3)

        gh_layer.process_layoff(gh_winner)

        # we lay off our single unmatched 5 against a set of 5's and expect a new deadwood count of 0
        self.assertEqual(gh_layer.deadwood_count(), 0)

    def test_process_layoff_single_meld(self):
        gh_layer = self.generate_ginhand_from_card_data(self.card_data6_layoff)
        gh_winner = self.generate_ginhand_from_card_data(self.card_data6)

        gh_layer.process_layoff(gh_winner)

        # we lay off our 2d, 4c, 8c, and 9h. this gives us an expected deadwood count of 14
        self.assertEqual(gh_layer.deadwood_count(), 14)
