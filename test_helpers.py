from ginhand import *
import unittest


# noinspection PyMethodMayBeStatic
class Helper(unittest.TestCase):

    card_data1 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (10, 's'),
        (11, 's'),
        (12, 's'),
        (13, 's'),
        (13, 'c'),
        (13, 'h'),
        (5, 'c'),
    ]

    card_data2 = [
        (9, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (10, 's'),
        (11, 's'),
        (12, 's'),
        (13, 's'),
        (13, 'c'),
        (13, 'h')
    ]

    card_data3 = [
        (1, 'h'),
        (9, 'c'),
        (9, 's'),
        (9, 'd'),
        (10, 's'),
        (11, 's'),
        (12, 's'),
        (5, 's'),
        (5, 'd'),
        (5, 'h')
    ]

    card_data4 = [
        (2, 'h'),
        (2, 'c'),
        (2, 'd'),
        (3, 'h'),
        (3, 's'),
        (3, 'c'),
        (4, 'c'),
        (5, 'c'),
        (11, 's'),
        (13, 'h')
    ]

    card_data5 = [
        (2, 'h'),
        (3, 'c'),
        (4, 's'),
        (5, 's'),
        (7, 's'),
        (8, 's'),
        (10, 's'),
        (13, 'c'),
        (13, 'h'),
        (13, 'd'),
    ]

    card_data6 = [
        (2, 'c'),
        (2, 's'),
        (2, 'h'),
        (5, 'c'),
        (6, 'c'),
        (7, 'c'),
        (10, 'h'),
        (11, 'h'),
        (12, 'h'),
        (13, 'h')
    ]

    card_data6_layoff = [
        (1, 'c'),
        (2, 'd'),
        (3, 'd'),
        (4, 'c'),
        (8, 'c'),
        (9, 'h'),
        (11, 's'),
        (12, 's'),
        (13, 's'),
        (13, 'd')
    ]

    card_data7 = [
        (1, 'c')
    ]

    #Everything in this group should be a part of a meld
    card_data9 = [
        (1, 's'),
        (2, 's'),
        (3, 's'),
        (2, 'h'),
        (3, 'h'),
        (4, 'h'),
        (5, 'h'),
        (13, 's'),
        (12, 's'),
        (11, 's'),
        (12, 'd'),
        (11, 'd'),
        (10, 'd')
    ]

    #Everything in this group should not have a meld
    card_data8 = [
        (1, 'c'),
        (2, 'd'),
        (13, 'd'),
        (12, 'c')
    ]

    @staticmethod
    def generate_ginhand_from_card_data(cdata):
        g = GinHand()
        for c in cdata:
            g.add_card(GinCard(c[0], c[1]))
        return g

    @staticmethod
    def generate_gincardgroup_from_card_data(cdata):
        cg = GinCardGroup()
        for c in cdata:
            cg.add_card(GinCard(c[0], c[1]))
        return cg

    # we pass in a control array (array of meld definitions like [(1, 'c'), (2, 'c'), (3, 'c')]) and
    # a test array of GinCardGroups. generate GinCardGroups for the control data and return true if they match.
    def compare_arrays_of_cardgroups(self, control_definitions, agcg_test):
        """
        @type agcg_test: GinCardGroup
        """

        agcg_control = []
        for meld_definition in control_definitions:
            agcg_control.append(GinCardGroup(meld_definition))

        for gcg in agcg_control:
            gcg.sort()
        for gcg in agcg_test:
            gcg.sort()

        # the number of GCG's must be the same
        self.assertEqual(len(agcg_control), len(agcg_test))

        self.assertEqual(0, len(list(set(agcg_test) - set(agcg_control))))

    def return_false(self):
        return False

    def return_true(self):
        return True
