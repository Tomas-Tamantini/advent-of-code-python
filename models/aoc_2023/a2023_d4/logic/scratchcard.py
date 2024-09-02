from dataclasses import dataclass


@dataclass(frozen=True)
class ScratchCard:
    card_id: int
    winning_numbers: set[int]
    chosen_numbers: set[int]

    @property
    def num_matches(self) -> int:
        return len(self.winning_numbers & self.chosen_numbers)
