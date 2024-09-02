from dataclasses import dataclass
import pytest
from ..scratchcard import ScratchCard, number_of_cards_after_prizes


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


@dataclass(frozen=True)
class _MockCard:
    num_matches: int = 0


def test_game_with_no_scratchcard_ends_up_with_no_cards():
    assert number_of_cards_after_prizes([]) == 0


def test_game_with_one_scratchcard_ends_up_with_one_card():
    assert number_of_cards_after_prizes([_MockCard()]) == 1


def test_scratchcard_yields_n_extra_cards_if_n_matches():
    cards = [_MockCard(num_matches=2), _MockCard(), _MockCard()]
    assert number_of_cards_after_prizes(cards) == 5


def test_yielding_extra_scratchcards_is_done_recursively():
    num_matches = [4, 2, 2, 1, 0, 0]
    cards = [_MockCard(num_matches=m) for m in num_matches]
    assert number_of_cards_after_prizes(cards) == 30
