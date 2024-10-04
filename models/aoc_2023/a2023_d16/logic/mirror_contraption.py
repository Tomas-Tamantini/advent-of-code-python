from typing import Iterator
from models.common.vectors import Vector2D, CardinalDirection
from .light_beam import LightBeam
from .contraption_cell import ContraptionCell, EmptyCell


class MirrorContraption:
    def __init__(self, width: int, height: int, cells: dict[Vector2D:ContraptionCell]):
        self._width = width
        self._height = height
        self._cells = cells

    @property
    def perimeter(self) -> int:
        return 2 * (self._width + self._height)

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    def propagate(self, beam: LightBeam) -> Iterator[LightBeam]:
        cell = self._cells.get(beam.position, EmptyCell())
        for new_direction in cell.next_directions(beam.direction):
            new_position = beam.position.move(new_direction, y_grows_down=True)
            if self._is_within_bounds(new_position):
                yield LightBeam(new_position, new_direction)

    def beams_starting_from_edges(self) -> Iterator[LightBeam]:
        for y in range(self._height):
            yield LightBeam(Vector2D(0, y), CardinalDirection.EAST)
            yield LightBeam(Vector2D(self._width - 1, y), CardinalDirection.WEST)
        for x in range(self._width):
            yield LightBeam(Vector2D(x, 0), CardinalDirection.SOUTH)
            yield LightBeam(Vector2D(x, self._height - 1), CardinalDirection.NORTH)
