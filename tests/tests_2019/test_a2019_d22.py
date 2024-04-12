import pytest
from models.aoc_2019 import (
    DealIntoNewStackShuffle,
    CutCardsShuffle,
    DealWithIncrementShuffle,
    MultiTechniqueShuffle,
)


@pytest.mark.parametrize(
    "position_before_shuffle, deck_size, expected_new_position",
    [(0, 10, 9), (2, 7, 4), (1234, 1235, 0)],
)
def test_dealing_into_new_stack_reverses_cards(
    position_before_shuffle, deck_size, expected_new_position
):
    shuffle = DealIntoNewStackShuffle(deck_size)
    new_position = shuffle.new_card_position(position_before_shuffle)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position",
    [(3, 2, 12345, 12344), (10, 0, 10, 0), (5, 6, 10, 1)],
)
def test_cutting_n_cards_sends_them_to_bottom(
    num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = CutCardsShuffle(deck_size, num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position",
    [(-4, 6, 10, 0), (-4, 3, 10, 7), (-1, 7, 1234, 8)],
)
def test_cutting_negative_num_cards_sends_bottom_ones_to_the_top(
    num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = CutCardsShuffle(deck_size, num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "increment, position_before_shuffle, deck_size, expected_new_position",
    [(1, 2, 1234, 2), (3, 7, 10, 1)],
)
def test_dealing_with_increment_spaces_cards_out_by_increment(
    increment, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = DealWithIncrementShuffle(deck_size, increment)
    new_position = shuffle.new_card_position(position_before_shuffle)
    assert new_position == expected_new_position


def test_multi_technique_shuffle_does_nothing_if_no_instructions():
    shuffle = MultiTechniqueShuffle(techniques=[])
    new_position = shuffle.new_card_position(7)
    assert new_position == 7


def test_multi_technique_shuffle_applies_shuffles_in_given_order():
    shuffle = MultiTechniqueShuffle(
        techniques=[
            DealIntoNewStackShuffle(deck_size=10),
            CutCardsShuffle(deck_size=10, num_cards_to_cut=-2),
            DealWithIncrementShuffle(deck_size=10, increment=7),
            CutCardsShuffle(deck_size=10, num_cards_to_cut=8),
            CutCardsShuffle(deck_size=10, num_cards_to_cut=-4),
            DealWithIncrementShuffle(deck_size=10, increment=7),
            CutCardsShuffle(deck_size=10, num_cards_to_cut=3),
            DealWithIncrementShuffle(deck_size=10, increment=9),
            DealWithIncrementShuffle(deck_size=10, increment=3),
            CutCardsShuffle(deck_size=10, num_cards_to_cut=-1),
        ]
    )
    assert shuffle.new_card_position(0) == 7
    assert shuffle.new_card_position(1) == 4
    assert shuffle.new_card_position(2) == 1
    assert shuffle.new_card_position(3) == 8
    assert shuffle.new_card_position(4) == 5
    assert shuffle.new_card_position(5) == 2
    assert shuffle.new_card_position(6) == 9
    assert shuffle.new_card_position(7) == 6
    assert shuffle.new_card_position(8) == 3
    assert shuffle.new_card_position(9) == 0
