from .camel_hand import CamelHand, first_hand_beats_second
from dataclasses import dataclass


@dataclass(frozen=True)
class CamelBid:
    hand: CamelHand
    bid_value: int

    def __lt__(self, other: "CamelBid") -> bool:
        return first_hand_beats_second(other.hand, self.hand)
