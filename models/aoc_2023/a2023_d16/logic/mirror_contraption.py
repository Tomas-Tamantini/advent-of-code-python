from typing import Iterator
from models.common.vectors import Vector2D
from .light_beam import LightBeam


class MirrorContraption:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    def propagate(self, beam: LightBeam) -> Iterator[LightBeam]:
        new_beam = beam.move_forward()
        if self._is_within_bounds(new_beam.position):
            yield new_beam
