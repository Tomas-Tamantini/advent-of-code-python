from typing import Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class _LinearCoefficients:
    first_degree: int
    zeroth_degree: int

    def compose(self, other: "_LinearCoefficients") -> "_LinearCoefficients":
        return _LinearCoefficients(
            first_degree=self.first_degree * other.first_degree,
            zeroth_degree=other.first_degree * self.zeroth_degree + other.zeroth_degree,
        )


class _LinearShuffle(Protocol):
    def new_card_position(
        self, position_before_shuffle: int, deck_size: int
    ) -> int: ...

    @property
    def linear_coefficients(self) -> _LinearCoefficients: ...


class DealIntoNewStackShuffle:
    def new_card_position(self, position_before_shuffle: int, deck_size: int) -> int:
        return deck_size - position_before_shuffle - 1

    @property
    def linear_coefficients(self) -> _LinearCoefficients:
        return _LinearCoefficients(-1, -1)


class CutCardsShuffle:
    def __init__(self, num_cards_to_cut: int) -> None:
        self._num_cards_to_cut = num_cards_to_cut

    def new_card_position(self, position_before_shuffle: int, deck_size: int) -> int:
        return (position_before_shuffle - self._num_cards_to_cut) % deck_size

    @property
    def linear_coefficients(self) -> _LinearCoefficients:
        return _LinearCoefficients(1, -self._num_cards_to_cut)


class DealWithIncrementShuffle:
    def __init__(self, increment: int) -> None:
        self._increment = increment

    def new_card_position(self, position_before_shuffle: int, deck_size: int) -> int:
        return (position_before_shuffle * self._increment) % deck_size

    @property
    def linear_coefficients(self) -> _LinearCoefficients:
        return _LinearCoefficients(self._increment, 0)


class MultiTechniqueShuffle:
    def __init__(self, techniques: list[_LinearShuffle]) -> None:
        self._linear_coefficients = _LinearCoefficients(1, 0)
        for technique in techniques:
            self._linear_coefficients = self._linear_coefficients.compose(
                technique.linear_coefficients
            )

    def new_card_position(self, position_before_shuffle: int, deck_size: int) -> int:
        return (
            self._linear_coefficients.first_degree * position_before_shuffle
            + self._linear_coefficients.zeroth_degree
        ) % deck_size
