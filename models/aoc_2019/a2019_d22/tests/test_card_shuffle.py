import pytest
from ..card_shuffle import (
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
    shuffle = DealIntoNewStackShuffle()
    new_position = shuffle.new_card_position(position_before_shuffle, deck_size)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position",
    [(3, 2, 12345, 12344), (10, 0, 10, 0), (5, 6, 10, 1)],
)
def test_cutting_n_cards_sends_them_to_bottom(
    num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = CutCardsShuffle(num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle, deck_size)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position",
    [(-4, 6, 10, 0), (-4, 3, 10, 7), (-1, 7, 1234, 8)],
)
def test_cutting_negative_num_cards_sends_bottom_ones_to_the_top(
    num_cards_to_cut, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = CutCardsShuffle(num_cards_to_cut)
    new_position = shuffle.new_card_position(position_before_shuffle, deck_size)
    assert new_position == expected_new_position


@pytest.mark.parametrize(
    "increment, position_before_shuffle, deck_size, expected_new_position",
    [(1, 2, 1234, 2), (3, 7, 10, 1)],
)
def test_dealing_with_increment_spaces_cards_out_by_increment(
    increment, position_before_shuffle, deck_size, expected_new_position
):
    shuffle = DealWithIncrementShuffle(increment)
    new_position = shuffle.new_card_position(position_before_shuffle, deck_size)
    assert new_position == expected_new_position


def test_multi_technique_shuffle_does_nothing_if_no_instructions():
    shuffle = MultiTechniqueShuffle(techniques=[])
    new_position = shuffle.new_card_position(7, deck_size=123)
    assert new_position == 7


example_shuffle = MultiTechniqueShuffle(
    techniques=[
        DealIntoNewStackShuffle(),
        CutCardsShuffle(num_cards_to_cut=-2),
        DealWithIncrementShuffle(increment=7),
        CutCardsShuffle(num_cards_to_cut=8),
        CutCardsShuffle(num_cards_to_cut=-4),
        DealWithIncrementShuffle(increment=7),
        CutCardsShuffle(num_cards_to_cut=3),
        DealWithIncrementShuffle(increment=9),
        DealWithIncrementShuffle(increment=3),
        CutCardsShuffle(num_cards_to_cut=-1),
    ]
)


def test_multi_technique_shuffle_applies_shuffles_in_given_order():
    deck_size = 10
    expected_positions = [7, 4, 1, 8, 5, 2, 9, 6, 3, 0]
    assert all(
        example_shuffle.new_card_position(i, deck_size) == expected_positions[i]
        for i in range(deck_size)
    )


def test_shuffle_can_be_reversed():
    deck_size = 10
    expected_positions = [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    assert all(
        example_shuffle.original_card_position(i, deck_size) == expected_positions[i]
        for i in range(deck_size)
    )


def test_shuffle_can_be_done_multiple_times():
    deck_size = 11
    num_shuffles = 100
    assert all(
        example_shuffle.new_card_position(
            example_shuffle.original_card_position(i, deck_size, num_shuffles),
            deck_size,
            num_shuffles,
        )
        == i
        for i in range(deck_size)
    )
