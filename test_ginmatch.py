from ginmatch import *
from test_helpers import *
from test_ginstrategy import MockGinStrategy


# noinspection PyProtectedMember
class TestGinMatch(Helper):

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

    def setUp(self):
        # set up the match
        self.p1 = GinPlayer()
        self.p2 = GinPlayer()
        self.gm = GinMatch(self.p1, self.p2)
        self.c = GinCard(2, 'c')

        self.p2.strategy = MockGinStrategy()

    def test__init__(self):
        # assign them to a match
        try:
            gm = GinMatch(self.p1, self.p2)
        except Exception:
            self.fail("Ginmatch() raised Exception unexpectedly!")

    def test_knock(self):
        self.gm.deal_cards()
        self.assertEqual(11, self.p1.hand.size())

        card_to_discard = self.p1.hand.cards[0]

        self.p1.knock(card_to_discard)
        self.assertEqual(10, self.p1.hand.size())
        self.assertFalse(self.p1.hand.contains_card(card_to_discard))

    # duplicate of test_knock
    def test_knock_gin(self):
        self.gm.deal_cards()
        self.assertEqual(11, self.p1.hand.size())

        card_to_discard = self.p1.hand.cards[0]

        self.p1.knock_gin(card_to_discard)
        self.assertEqual(10, self.p1.hand.size())
        self.assertFalse(self.p1.hand.contains_card(card_to_discard))

    def test_notify_of_knock(self):
        self.p1.knock(self.c)
        self.assertEqual(self.gm.player_who_knocked, self.p1)

    def test_notify_of_knock_gin(self):
        self.p1.knock_gin(self.c)
        self.assertEqual(self.gm.player_who_knocked_gin, self.p1)

    def test_organize_data(self):
        data = self.gm.organize_data()

        # we expect 5 values: player scores (p1,2p), player matches won (p1, p2) and knock point
        self.assertEqual(5, len(data.keys()))

        # knock point initializes as 10
        self.assertEqual(10, data[0])

        # scores and matches won initialize as 0
        self.assertEqual(0, data[1])
        self.assertEqual(0, data[2])
        self.assertEqual(0, data[3])
        self.assertEqual(0, data[4])

    def test_run(self):
        # rig the horse with rockets
        self.gm.p1_score = 100
        self.gm.p1_games_won = 1

        # run the match and return the winner.
        match_result = self.gm.run()
        winner                    = match_result['winner']
        loser                     = match_result['loser']
        winner_wins               = match_result['winner_games_won']
        winner_wins_by_coinflip   = match_result['winner_games_won_by_coinflip']
        winner_losses             = match_result['winner_games_lost']
        loser_wins                = match_result['loser_games_won']
        loser_wins_by_coinflip    = match_result['loser_games_won_by_coinflip']
        loser_losses              = match_result['loser_games_lost']
        winner_point_delta        = match_result['winner_point_delta']

        # make sure the winner is our horse
        self.assertEqual(winner, self.p1)
        self.assertEqual(loser,  self.p2)
        self.assertEqual(winner_wins_by_coinflip, 0)
        self.assertEqual(loser_wins_by_coinflip, 0)

        self.assertEqual(winner_losses, 0)
        self.assertEqual(loser_losses, 1)

        self.assertEqual(winner_point_delta, 220)

        # give strategies that guarantee a coinflip ending
        self.gm = GinMatch(self.p1, self.p2)
        strat_code = {'start': ['DRAW'], 'end': ['DISCARD', 0]}
        self.p1.strategy = MockGinStrategy(strat_code)
        self.p2.strategy = MockGinStrategy(strat_code)

        match_result = self.gm.run()
        winner_wins_by_coinflip      = match_result['winner_games_won_by_coinflip']
        loser_wins_by_coinflip       = match_result['winner_games_won_by_coinflip']
        self.assertGreaterEqual(winner_wins_by_coinflip + loser_wins_by_coinflip, 2)


    def test_play_game(self):
        # all play_game does is reset some flags and call other methods. leaving it blank.
        pass

    def test_deal_cards(self):
        # assert player 1 receives 11 cards and player 2 receives 10 cards
        self.gm.deal_cards()

        self.assertEqual(11, self.p1.hand.size())
        self.assertEqual(10, self.p2.hand.size())

    def test_take_turns(self):
        # set up the match. we'll give p1 a gin-worthy hand and p2 a knock-worth hand (deadwood=1)
        self.p1 = GinPlayer()
        self.p2 = GinPlayer()
        self.gm = GinMatch(self.p1, self.p2)
        self.p1.strategy = MockGinStrategy({'end': ['KNOCK', 10]})

        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_0_deadwood)
        # give p1 an 11th card for discarding
        self.p1.hand.add_card(GinCard(1, 'h'))
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # after turn taking is done, we should reach the gameover state and have exactly one knocker
        self.gm.take_turns()
        self.assertTrue(self.gm.gameover)
        someone_knocked = self.gm.player_who_knocked != False
        someone_knocked_gin = self.gm.player_who_knocked_gin != False
        # use an xor to ensure we only had one knock
        self.assertTrue(someone_knocked ^ someone_knocked_gin)

    def test_end_with_knock_invalid(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # if the knock was INVALID, ensure we penalize the player by exposing his cards
        self.gm.process_knock(self.p1)
        self.assertTrue(self.gm.p1_knocked_improperly)
        self.assertFalse(self.gm.player_who_knocked)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p1)

    def test_knock_invalid_11points(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_11_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # if the knock was INVALID, ensure we penalize the player by exposing his cards
        self.gm.process_knock(self.p1)
        self.assertTrue(self.gm.p1_knocked_improperly)
        self.assertFalse(self.gm.player_who_knocked)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p1)

    def test_process_knock_valid_10points(self):
        self.p1 = GinPlayer()
        self.p2 = GinPlayer()
        self.gm = GinMatch(self.p1, self.p2)

        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # if the knock was VALID, ensure we mark the game as over
        self.gm.process_knock(self.p2)
        self.assertFalse(self.gm.p2_knocked_improperly)
        self.assertTrue(self.gm.gameover)
        self.assertEqual(self.gm.player_who_knocked, self.p2)
        self.assertEqual(self.gm.player_who_knocked, self.p2)

    def test_process_knock_valid_1point(self):
        self.p1 = GinPlayer()
        self.p2 = GinPlayer()
        self.gm = GinMatch(self.p1, self.p2)

        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)

        # if the knock was VALID, ensure we mark the game as over
        self.gm.process_knock(self.p2)
        self.assertFalse(self.gm.p2_knocked_improperly)
        self.assertTrue(self.gm.gameover)
        self.assertEqual(self.gm.player_who_knocked, self.p2)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p2)

    def test_process_knock_valid_0points(self):
        self.p1 = GinPlayer()
        self.p2 = GinPlayer()
        self.gm = GinMatch(self.p1, self.p2)

        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)

        # if the knock was VALID, ensure we mark the game as over
        self.gm.process_knock(self.p2)
        self.assertFalse(self.gm.p2_knocked_improperly)
        self.assertTrue(self.gm.gameover)
        self.assertEqual(self.gm.player_who_knocked, self.p2)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p2)

    def test_process_knock_gin_invalid_55points(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)

        # if the knock was INVALID, ensure we penalize the player by exposing the cards (also, gameover is not yet set)
        self.gm.process_knock_gin(self.p1)
        self.assertTrue(self.gm.p1_knocked_improperly)
        self.assertFalse(self.gm.player_who_knocked)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p1)

    def test_process_knock_gin_invalid_11points(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_11_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # if the knock was INVALID, ensure we penalize the player by exposing the cards (also, gameover is not yet set)
        self.gm.process_knock_gin(self.p1)
        self.assertTrue(self.gm.p1_knocked_improperly)
        self.assertFalse(self.gm.player_who_knocked)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p1)

    def test_process_knock_gin_valid_10points(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # gin-worthy hand with deadwood=10
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)

        # if the knock was VALID, ensure we penalize the player and that the game continues
        self.gm.process_knock_gin(self.p2)
        self.assertTrue(self.gm.p2_knocked_improperly)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p2)
        self.assertFalse(self.gm.gameover)

    def test_process_knock_gin_valid_1point(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # gin-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)

        # if the knock was VALID, ensure we penalize the player and that the game continues
        self.gm.process_knock_gin(self.p2)
        self.assertTrue(self.gm.p2_knocked_improperly)
        self.assertNotEqual(self.gm.player_who_knocked_gin, self.p2)
        self.assertFalse(self.gm.gameover)

    def test_process_knock_gin_valid_0points(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # gin-worthy hand with deadwood=0
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_0_deadwood)

        # if the knock was VALID, ensure we penalize the player and that the game continues
        self.gm.process_knock_gin(self.p2)
        self.assertFalse(self.gm.p2_knocked_improperly)
        self.assertEqual(self.gm.player_who_knocked_gin, self.p2)
        self.assertNotEqual(self.gm.player_who_knocked, self.p2)
        self.assertTrue(self.gm.gameover)

    def test_end_game_with_coinflip(self):
        self.assertEqual(0, self.gm.p1_wins_by_coinflip + self.gm.p2_wins_by_coinflip)
        self.assertFalse(self.gm.player_who_won_coinflip)
        self.gm.end_game_with_coinflip()
        self.gm.update_score()
        self.assertEqual(1, self.gm.p1_wins_by_coinflip + self.gm.p2_wins_by_coinflip)
        self.assertTrue(self.gm.player_who_won_coinflip)

    def test_update_score_for_gin(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # gin-worthy hand with deadwood=0
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_0_deadwood)

        # add a card to discard
        dummy_card = GinCard(2, 'd')
        self.p2._add_card(dummy_card)

        # knock
        self.p2.knock_gin(dummy_card)

        self.gm.update_score()
        self.assertEqual(self.gm.p1_score, 0)
        self.assertEqual(self.gm.p2_score, 55+25)

    def test_update_score_for_knock(self):
        # morbidly awful hand with deadwood = 55
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_55_deadwood)

        # knock-worthy hand with deadwood=1
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)

        # add a card to discard
        dummy_card = GinCard(2, 'd')
        self.p2._add_card(dummy_card)

        # knock
        self.p2.knock(dummy_card)

        self.gm.update_score()
        self.assertEqual(self.gm.p1_score, 0)
        self.assertEqual(self.gm.p2_score, 54)

    def test_update_score_with_knock_undercut(self):
        # knock-worthy hand with deadwood=1
        self.p1.hand = self.generate_ginhand_from_card_data(self.hand_1_deadwood)
        dummy_card = GinCard(2, 'd')
        self.p1._add_card(dummy_card)

        # for whatever reason, p2 decided to bm by not knocking gin
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_0_deadwood)

        # p1 knocks, believing he has the best hand
        self.p1.knock(dummy_card)

        self.gm.update_score()

        # verify that p2 gets the undercut bonus AND the deadwood points
        self.assertEqual(self.gm.p1_score, 0)
        self.assertEqual(self.gm.p2_score, 1+25)

    def test_offer_to_accept_improper_knock(self):
        # set up the improper knock conditions (here p1 knocks with deadwood=55, while p2 holds deadwood=1)
        self.test_process_knock_gin_invalid_55points()

        # we force p2 to ACCEPT the knock
        self.p2.strategy.accept_improper_knock = self.return_true
        result = self.gm.offer_to_accept_improper_knock(self.p2)
        self.assertTrue(result)

        # ensure the game HAS been marked as over
        self.assertTrue(self.gm.gameover)

    def test_offer_to_accept_improper_knock_ineligible_accepter(self):
        # set up the improper knock conditions (here p1 knocks with deadwood=55, while p2 holds deadwood=37)
        self.test_process_knock_gin_invalid_55points()
        self.p2.hand = self.generate_ginhand_from_card_data(self.card_data6_layoff)
        self.assertTrue(self.p2.hand.deadwood_count() > 10)
        self.gm.gameover = False

        # we instruct p2 to REJECT the knock
        self.p2.strategy.accept_improper_knock = self.return_false
        self.gm.offer_to_accept_improper_knock(self.p2)

        # ensure the game has NOT been marked as over
        self.assertFalse(self.gm.gameover)

    # note: while this looks similar to test_offer_to_accept_improper_knock_invalid, in this case we expect the
    # rejection to actually take place, whereas in the prior test, there is no option to reject due to p2's high
    # deadwood count.
    def test_offer_to_accept_improper_knock_decline(self):
        # set up the improper knock conditions (here p1 knocks with deadwood=55, while p2 holds deadwood=1)
        self.test_process_knock_gin_invalid_55points()
        self.p2.hand = self.generate_ginhand_from_card_data(self.hand_10_deadwood)
        self.gm.gameover = False

        # we instruct p2 to REJECT the knock
        self.p2.accept_improper_knock = self.return_false
        result = self.gm.offer_to_accept_improper_knock(self.p2)
        self.assertFalse(result)

        # ensure the game has NOT been marked as over
        self.assertFalse(self.gm.gameover)

    def test_get_player_string(self):
        self.assertEqual(self.gm.get_player_string(self.p1), "player 1")
        self.assertEqual(self.gm.get_player_string(self.p2), "player 2")
