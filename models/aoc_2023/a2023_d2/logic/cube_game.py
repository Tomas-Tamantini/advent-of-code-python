from typing import Iterable
from .cube_amount import CubeAmount


class CubeGame:
    def __init__(self, handfuls: Iterable[CubeAmount]) -> None:
        self._handfuls = handfuls

    def bag_amount_is_possible(self, bag: CubeAmount) -> bool:
        return all(handful.all_colors_leq(bag) for handful in self._handfuls)
