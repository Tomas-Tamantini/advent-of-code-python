import pytest
from ..logic import ScratchCard


def test_scratchcard_keeps_track_of_number_of_matching_numbers():
    card = ScratchCard(
        card_id=123, winning_numbers={1, 2, 3}, chosen_numbers={1, 3, 5, 7}
    )
    assert card.num_matches == 2


def test_scratchcard_with_no_matches_is_worth_zero_points():
    card = ScratchCard(card_id=123, winning_numbers={1, 2, 3}, chosen_numbers={4, 5, 6})
    assert card.num_points() == 0


@pytest.mark.parametrize("num_matches, num_points", [(1, 1), (2, 2), (3, 4), (10, 512)])
def test_scratchcard_with_n_matches_is_worth_n_minus_one_power_of_two_points(
    num_matches, num_points
):
    numbers = set(range(num_matches))
    card = ScratchCard(card_id=123, winning_numbers=numbers, chosen_numbers=numbers)
    assert card.num_points() == num_points
