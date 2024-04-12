from typing import Protocol


class _Shuffle(Protocol):
    def new_card_position(
        self, position_before_shuffle: int, total_num_cards: int
    ) -> int: ...


class DealIntoNewStackShuffle:
    def new_card_position(
        self, position_before_shuffle: int, total_num_cards: int
    ) -> int:
        return total_num_cards - position_before_shuffle - 1


class CutCardsShuffle:
    def __init__(self, num_cards_to_cut: int) -> None:
        self._num_cards_to_cut = num_cards_to_cut

    def new_card_position(
        self, position_before_shuffle: int, total_num_cards: int
    ) -> int:
        return (position_before_shuffle - self._num_cards_to_cut) % total_num_cards


class DealWithIncrementShuffle:
    def __init__(self, increment: int) -> None:
        self._increment = increment

    def new_card_position(
        self, position_before_shuffle: int, total_num_cards: int
    ) -> int:
        return (position_before_shuffle * self._increment) % total_num_cards


class MultiTechniqueShuffle:
    def __init__(self, techniques: list[_Shuffle]) -> None:
        self._techniques = techniques

    def new_card_position(
        self, position_before_shuffle: int, total_num_cards: int
    ) -> int:
        for technique in self._techniques:
            position_before_shuffle = technique.new_card_position(
                position_before_shuffle, total_num_cards
            )
        return position_before_shuffle
