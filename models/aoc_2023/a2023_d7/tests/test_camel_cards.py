from ..logic import HandRank


def test_hand_ranks_are_properly_ordered():
    assert HandRank.HIGH_CARD < HandRank.ONE_PAIR
    assert HandRank.ONE_PAIR < HandRank.TWO_PAIRS
    assert HandRank.TWO_PAIRS < HandRank.THREE_OF_A_KIND
    assert HandRank.THREE_OF_A_KIND < HandRank.FULL_HOUSE
    assert HandRank.FULL_HOUSE < HandRank.FOUR_OF_A_KIND
    assert HandRank.FOUR_OF_A_KIND < HandRank.FIVE_OF_A_KIND
