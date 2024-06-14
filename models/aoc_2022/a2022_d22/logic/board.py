from typing import Protocol
from models.common.vectors import Vector2D
from .board_navigator import BoardNavigator


class Board(Protocol):
    @property
    def initial_position(self) -> Vector2D: ...

    def next_position(self, navigator: BoardNavigator, num_steps: int) -> Vector2D: ...
