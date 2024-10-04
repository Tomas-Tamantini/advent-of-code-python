from typing import Iterator
from models.common.vectors import Vector2D
from .light_beam import LightBeam
from .contraption_cell import ContraptionCell, EmptyCell


class MirrorContraption:
    def __init__(self, width: int, height: int, cells: dict[Vector2D:ContraptionCell]):
        self._width = width
        self._height = height
        self._cells = cells

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    def propagate(self, beam: LightBeam) -> Iterator[LightBeam]:
        cell = self._cells.get(beam.position, EmptyCell())
        for new_direction in cell.next_directions(beam.direction):
            new_position = beam.position.move(new_direction, y_grows_down=True)
            if self._is_within_bounds(new_position):
                yield LightBeam(new_position, new_direction)
