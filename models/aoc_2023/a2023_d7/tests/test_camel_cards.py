import pytest
from ..logic import HandRank, OrdinaryHand, JokerHand, first_hand_beats_second, CamelBid


def test_hand_ranks_are_properly_ordered():
    assert HandRank.HIGH_CARD < HandRank.ONE_PAIR
    assert HandRank.ONE_PAIR < HandRank.TWO_PAIRS
    assert HandRank.TWO_PAIRS < HandRank.THREE_OF_A_KIND
    assert HandRank.THREE_OF_A_KIND < HandRank.FULL_HOUSE
    assert HandRank.FULL_HOUSE < HandRank.FOUR_OF_A_KIND
    assert HandRank.FOUR_OF_A_KIND < HandRank.FIVE_OF_A_KIND


@pytest.mark.parametrize(
    "hand, rank",
    [
        ("23456", HandRank.HIGH_CARD),
        ("A23A4", HandRank.ONE_PAIR),
        ("23432", HandRank.TWO_PAIRS),
        ("TTT98", HandRank.THREE_OF_A_KIND),
        ("23332", HandRank.FULL_HOUSE),
        ("AAJAA", HandRank.FOUR_OF_A_KIND),
        ("AAAAA", HandRank.FIVE_OF_A_KIND),
    ],
)
def test_ordinary_hands_properly_classify_rank(hand, rank):
    assert OrdinaryHand(hand).rank() == rank


def test_ordinary_hands_properly_classify_card_values():
    assert tuple(OrdinaryHand("29TJA").card_values()) == (2, 9, 10, 11, 14)


@pytest.mark.parametrize(
    "hand, rank",
    [
        ("23456", HandRank.HIGH_CARD),
        ("23J56", HandRank.ONE_PAIR),
        ("KKQQ6", HandRank.TWO_PAIRS),
        ("7J9TJ", HandRank.THREE_OF_A_KIND),
        ("7788J", HandRank.FULL_HOUSE),
        ("QJJQ2", HandRank.FOUR_OF_A_KIND),
        ("AAAJJ", HandRank.FIVE_OF_A_KIND),
        ("JJJJJ", HandRank.FIVE_OF_A_KIND),
    ],
)
def test_joker_hands_properly_classify_rank(hand, rank):
    assert JokerHand(hand).rank() == rank


def test_joker_hands_properly_classify_card_values():
    assert tuple(JokerHand("38QKJ").card_values()) == (3, 8, 12, 13, 0)


def test_hand_of_higher_rank_beats_hand_of_lower_rank():
    best = OrdinaryHand("AAAJJ")
    worst = OrdinaryHand("TTT98")
    assert first_hand_beats_second(best, worst)
    assert not first_hand_beats_second(worst, best)


def test_hands_with_same_ranks_are_compared_card_by_card_from_first_to_last():
    best = OrdinaryHand("3256T")
    worst = OrdinaryHand("3254T")
    assert first_hand_beats_second(best, worst)
    assert not first_hand_beats_second(worst, best)


def test_camel_bids_can_be_sorted():
    bids = [
        CamelBid(hand=OrdinaryHand("3256T"), bid_value=1),
        CamelBid(hand=OrdinaryHand("AAAJJ"), bid_value=2),
        CamelBid(hand=OrdinaryHand("3254T"), bid_value=3),
    ]
    sorted_values = [bid.bid_value for bid in sorted(bids)]
    assert sorted_values == [3, 1, 2]
