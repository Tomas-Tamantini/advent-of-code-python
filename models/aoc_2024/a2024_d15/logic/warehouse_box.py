from dataclasses import dataclass
from typing import Iterator, Protocol

from models.common.vectors import Vector2D


class WarehouseBox(Protocol):
    @property
    def origin_position(self) -> Vector2D: ...

    def positions(self) -> Iterator[Vector2D]: ...

    def move(self, direction: Vector2D) -> "WarehouseBox": ...


@dataclass(frozen=True)
class SingleWidthBox:
    origin_position: Vector2D

    def positions(self) -> Iterator[Vector2D]:
        yield self.origin_position

    def move(self, direction: Vector2D) -> "SingleWidthBox":
        return SingleWidthBox(self.origin_position.move(direction, y_grows_down=True))


class WarehouseBoxes:
    def __init__(self, boxes: set[WarehouseBox]):
        self._boxes = boxes

    def box_positions(self) -> Iterator[Vector2D]:
        yield from (box.origin_position for box in self._boxes)

    def _box_at(self, position: Vector2D) -> WarehouseBox | None:
        for box in self._boxes:
            if box.origin_position == position:
                return box
        return None

    def boxes_in_front(
        self, position: Vector2D, direction: Vector2D
    ) -> Iterator[WarehouseBox]:
        stack = [position]
        visited = set()
        while stack:
            current_pos = stack.pop().move(direction, y_grows_down=True)
            box = self._box_at(current_pos)
            if box and box not in visited:
                visited.add(box)
                yield box
                for pos in box.positions():
                    stack.append(pos)

    def move_boxes(
        self, boxes: set[WarehouseBox], direction: Vector2D
    ) -> "WarehouseBoxes":
        new_boxes = self._boxes - boxes | {box.move(direction) for box in boxes}
        return WarehouseBoxes(new_boxes)
