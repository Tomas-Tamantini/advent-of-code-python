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
