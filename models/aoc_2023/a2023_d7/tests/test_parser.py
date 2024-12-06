import pytest

from models.common.io import InputFromString

from ..logic import HandRank
from ..parser import parse_camel_bids


@pytest.mark.parametrize("include_joker", [True, False])
def test_parse_camel_bids_with_or_without_jokers(include_joker):
    file_content = """32T3K 765
                      T55J5 684"""
    input_reader = InputFromString(file_content)
    bids = list(parse_camel_bids(input_reader, include_joker))
    assert len(bids) == 2
    assert [bid.bid_value for bid in bids] == [765, 684]
    assert tuple(bids[0].hand.card_values()) == (3, 2, 10, 3, 13)
    assert (
        bids[1].hand.rank() == HandRank.FOUR_OF_A_KIND
        if include_joker
        else HandRank.THREE_OF_A_KIND
    )
