import pytest
from models.aoc_2019 import (
    DealIntoNewStackShuffle,
    CutCardsShuffle,
    DealWithIncrementShuffle,
    MultiTechniqueShuffle,
)


@pytest.mark.parametrize(
    "position_before_shuffle, total_num_cards, expected_new_position",
    [(0, 10, 9), (2, 7, 4), (1234, 1235, 0)],
)
def test_dealing_into_new_stack_reverses_cards(
    position_before_shuffle, total_num_cards, expected_new_position
):
    shuffle = DealIntoNewStackShuffle()
    new_position = shuffle.new_card_position(position_before_shuffle, total_num_cards)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, total_num_cards, expected_new_position",
    [(3, 2, 12345, 12344), (10, 0, 10, 0), (5, 6, 10, 1)],
)
def test_cutting_n_cards_sends_them_to_bottom(
    num_cards_to_cut, position_before_shuffle, total_num_cards, expected_new_position
):
    shuffle = CutCardsShuffle(num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle, total_num_cards)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, total_num_cards, expected_new_position",
    [(-4, 6, 10, 0), (-4, 3, 10, 7), (-1, 7, 1234, 8)],
)
def test_cutting_negative_num_cards_sends_bottom_ones_to_the_top(
    num_cards_to_cut, position_before_shuffle, total_num_cards, expected_new_position
):
    shuffle = CutCardsShuffle(num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle, total_num_cards)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "increment, position_before_shuffle, total_num_cards, expected_new_position",
    [(1, 2, 1234, 2), (3, 7, 10, 1)],
)
def test_dealing_with_increment_spaces_cards_out_by_increment(
    increment, position_before_shuffle, total_num_cards, expected_new_position
):
    shuffle = DealWithIncrementShuffle(increment)
    new_position = shuffle.new_card_position(position_before_shuffle, total_num_cards)
    assert new_position == expected_new_position


def test_multi_technique_shuffle_does_nothing_if_no_instructions():
    shuffle = MultiTechniqueShuffle(techniques=[])
    new_position = shuffle.new_card_position(7, 10)
    assert new_position == 7


def test_multi_technique_shuffle_applies_shuffles_in_given_order():
    shuffle = MultiTechniqueShuffle(
        techniques=[
            DealIntoNewStackShuffle(),
            CutCardsShuffle(-2),
            DealWithIncrementShuffle(7),
            CutCardsShuffle(8),
            CutCardsShuffle(-4),
            DealWithIncrementShuffle(7),
            CutCardsShuffle(3),
            DealWithIncrementShuffle(9),
            DealWithIncrementShuffle(3),
            CutCardsShuffle(-1),
        ]
    )
    assert shuffle.new_card_position(0, 10) == 7
    assert shuffle.new_card_position(1, 10) == 4
    assert shuffle.new_card_position(2, 10) == 1
    assert shuffle.new_card_position(3, 10) == 8
    assert shuffle.new_card_position(4, 10) == 5
    assert shuffle.new_card_position(5, 10) == 2
    assert shuffle.new_card_position(6, 10) == 9
    assert shuffle.new_card_position(7, 10) == 6
    assert shuffle.new_card_position(8, 10) == 3
    assert shuffle.new_card_position(9, 10) == 0
