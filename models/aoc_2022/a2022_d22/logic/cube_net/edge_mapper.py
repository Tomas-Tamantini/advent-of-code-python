from typing import Protocol

from .cube_navigator import CubeNavigator


class EdgeMapper(Protocol):
    def next_navigator(self, navigator: CubeNavigator) -> CubeNavigator: ...
