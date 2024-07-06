from typing import Iterable
from .cube_amount import CubeAmount


class CubeGame:
    def __init__(self, game_id: int, handfuls: Iterable[CubeAmount]) -> None:
        self._id = game_id
        self._handfuls = handfuls

    @property
    def game_id(self) -> int:
        return self._id

    @property
    def handfuls(self) -> Iterable[CubeAmount]:
        return self._handfuls

    def minimum_bag(self) -> CubeAmount:
        return CubeAmount.merge(*self._handfuls)

    def bag_amount_is_possible(self, bag: CubeAmount) -> bool:
        return all(handful.all_colors_leq(bag) for handful in self._handfuls)
