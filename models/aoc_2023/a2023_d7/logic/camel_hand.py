from collections import defaultdict
from typing import Protocol, Iterator
from .hand_rank import HandRank, get_rank


class CamelHand(Protocol):
    def rank(self) -> HandRank: ...

    def card_values(self) -> Iterator[int]: ...


class OrdinaryHand:
    def __init__(self, cards: str) -> None:
        self._cards = cards

    def rank(self) -> HandRank:
        card_count = defaultdict(int)
        for card in self._cards:
            card_count[card] += 1
        return get_rank(
            highest_multiplicity=max(card_count.values()),
            num_card_values=len(card_count),
        )

    @staticmethod
    def _card_value(card: chr) -> int:
        face_values = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        return face_values[card] if card in face_values else int(card)

    def card_values(self) -> Iterator[int]:
        return map(self._card_value, self._cards)


class JokerHand:
    def __init__(self, cards: str) -> None:
        self._cards = cards

    def rank(self) -> HandRank:
        card_count = defaultdict(int)
        num_jokers = 0
        for card in self._cards:
            if card == "J":
                num_jokers += 1
            else:
                card_count[card] += 1
        num_card_values = len(card_count)
        if num_card_values == 0:
            return HandRank.FIVE_OF_A_KIND
        highest_multiplicity = max(card_count.values()) + num_jokers
        return get_rank(highest_multiplicity, num_card_values)

    @staticmethod
    def _card_value(card: chr) -> int:
        face_values = {"T": 10, "J": 0, "Q": 12, "K": 13, "A": 14}
        return face_values[card] if card in face_values else int(card)

    def card_values(self) -> Iterator[int]:
        return map(self._card_value, self._cards)
