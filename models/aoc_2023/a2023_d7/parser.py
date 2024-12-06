from typing import Iterator

from models.common.io import InputReader

from .logic import CamelBid, JokerHand, OrdinaryHand


def _parse_bid(line: str, include_joker: bool) -> CamelBid:
    cards, bid_value = line.split()
    hand = JokerHand(cards) if include_joker else OrdinaryHand(cards)
    return CamelBid(hand, int(bid_value))


def parse_camel_bids(
    input_reader: InputReader, include_joker: bool
) -> Iterator[CamelBid]:
    for line in input_reader.read_stripped_lines():
        yield _parse_bid(line, include_joker)
