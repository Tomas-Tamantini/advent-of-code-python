from typing import Protocol


class _Shuffle(Protocol):
    def new_card_position(
        self, current_card_position: int, total_num_cards: int
    ) -> int: ...


class DealIntoNewStackShuffle:
    def new_card_position(
        self, current_card_position: int, total_num_cards: int
    ) -> int:
        return total_num_cards - current_card_position - 1


class CutCardsShuffle:
    def __init__(self, num_cards_to_cut: int) -> None:
        self._num_cards_to_cut = num_cards_to_cut

    def new_card_position(
        self, current_card_position: int, total_num_cards: int
    ) -> int:
        return (current_card_position - self._num_cards_to_cut) % total_num_cards


class DealWithIncrementShuffle:
    def __init__(self, increment: int) -> None:
        self._increment = increment

    def new_card_position(
        self, current_card_position: int, total_num_cards: int
    ) -> int:
        return (current_card_position * self._increment) % total_num_cards


class MultiTechniqueShuffle:
    def __init__(self, techniques: list[_Shuffle]) -> None:
        self._techniques = techniques

    def new_card_position(
        self, current_card_position: int, total_num_cards: int
    ) -> int:
        for technique in self._techniques:
            current_card_position = technique.new_card_position(
                current_card_position, total_num_cards
            )
        return current_card_position
