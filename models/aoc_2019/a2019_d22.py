from typing import Protocol


class _Shuffle(Protocol):
    def new_card_position(self, position_before_shuffle: int) -> int: ...


class DealIntoNewStackShuffle:
    def __init__(self, deck_size: int) -> None:
        self._deck_size = deck_size

    def new_card_position(self, position_before_shuffle: int) -> int:
        return self._deck_size - position_before_shuffle - 1


class CutCardsShuffle:
    def __init__(self, deck_size: int, num_cards_to_cut: int) -> None:
        self._deck_size = deck_size
        self._num_cards_to_cut = num_cards_to_cut

    def new_card_position(self, position_before_shuffle: int) -> int:
        return (position_before_shuffle - self._num_cards_to_cut) % self._deck_size


class DealWithIncrementShuffle:
    def __init__(self, deck_size: int, increment: int) -> None:
        self._deck_size = deck_size
        self._increment = increment

    def new_card_position(self, position_before_shuffle: int) -> int:
        return (position_before_shuffle * self._increment) % self._deck_size


class MultiTechniqueShuffle:
    def __init__(self, techniques: list[_Shuffle]) -> None:
        self._techniques = techniques

    def new_card_position(self, position_before_shuffle: int) -> int:
        for technique in self._techniques:
            position_before_shuffle = technique.new_card_position(
                position_before_shuffle
            )
        return position_before_shuffle
