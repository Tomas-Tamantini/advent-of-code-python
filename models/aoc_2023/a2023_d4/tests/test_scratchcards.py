from ..logic import ScratchCard


def test_scratchcard_keeps_track_of_number_of_matching_numbers():
    card = ScratchCard(
        card_id=123, winning_numbers={1, 2, 3}, chosen_numbers={1, 3, 5, 7}
    )
    assert card.num_matches == 2
