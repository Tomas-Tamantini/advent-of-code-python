from typing import Iterator
from models.common.vectors import Vector3D


class _BoundingBox3D:
    def __init__(self, positions: set[Vector3D]) -> None:
        self._min = Vector3D(
            min(pos.x for pos in positions),
            min(pos.y for pos in positions),
            min(pos.z for pos in positions),
        ) - Vector3D(1, 1, 1)

        self._max = Vector3D(
            max(pos.x for pos in positions),
            max(pos.y for pos in positions),
            max(pos.z for pos in positions),
        ) + Vector3D(1, 1, 1)

    @property
    def min_position(self) -> Vector3D:
        return self._min

    def contains(self, position: Vector3D) -> bool:
        return (
            self._min.x <= position.x <= self._max.x
            and self._min.y <= position.y <= self._max.y
            and self._min.z <= position.z <= self._max.z
        )


def _valid_neighbors(
    current_cell: Vector3D, bounding_box: _BoundingBox3D
) -> Iterator[Vector3D]:
    for neighbor in current_cell.adjacent_positions(include_diagonals=False):
        if bounding_box.contains(neighbor):
            yield neighbor


def external_surface_area(cubes: set[Vector3D]) -> int:
    if not cubes:
        return 0
    bounding_box = _BoundingBox3D(cubes)
    initial_air_cell = bounding_box.min_position
    flood_fill_stack = [initial_air_cell]
    visited = {initial_air_cell}
    surface_area = 0
    while flood_fill_stack:
        current_cell = flood_fill_stack.pop()
        for neighbor in _valid_neighbors(current_cell, bounding_box):
            if neighbor in cubes:
                surface_area += 1
            elif neighbor not in visited:
                flood_fill_stack.append(neighbor)
                visited.add(neighbor)

    return surface_area
