from dataclasses import dataclass


@dataclass(frozen=True)
class ScratchCard:
    card_id: int
    winning_numbers: set[int]
    chosen_numbers: set[int]

    @property
    def num_matches(self) -> int:
        return len(self.winning_numbers & self.chosen_numbers)

    def num_points(self) -> int:
        return 0 if self.num_matches == 0 else 2 ** (self.num_matches - 1)


def _range_of_cards_to_copy(current_card_idx: int, cards: list[ScratchCard]) -> range:
    current_card = cards[current_card_idx]
    range_start = current_card_idx + 1
    range_end = min(current_card_idx + 1 + current_card.num_matches, len(cards))
    return range(range_start, range_end)


def number_of_cards_after_prizes(cards: list[ScratchCard]) -> int:
    multiplicity = [1] * len(cards)
    for i in range(len(cards)):
        for j in _range_of_cards_to_copy(i, cards):
            multiplicity[j] += multiplicity[i]
    return sum(multiplicity)
