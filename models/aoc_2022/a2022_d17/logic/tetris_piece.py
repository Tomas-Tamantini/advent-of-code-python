from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class TetrisPiece:
    shape: tuple[Vector2D, ...]
    offset: Vector2D

    def positions(self) -> Iterator[Vector2D]:
        for position in self.shape:
            yield position + self.offset

    def move(self, direction: Vector2D) -> "TetrisPiece":
        return TetrisPiece(shape=self.shape, offset=self.offset.move(direction))
