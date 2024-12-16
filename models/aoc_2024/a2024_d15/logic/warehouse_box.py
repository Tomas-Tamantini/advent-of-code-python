from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class SingleWidthBox:
    origin_position: Vector2D

    def positions(self) -> Iterator[Vector2D]:
        yield self.origin_position

    def move(self, direction: CardinalDirection) -> "SingleWidthBox":
        return SingleWidthBox(self.origin_position.move(direction, y_grows_down=True))

    @staticmethod
    def from_position(position: Vector2D) -> Iterator["SingleWidthBox"]:
        yield SingleWidthBox(position)


@dataclass(frozen=True)
class DoubleWidthBox:
    origin_position: Vector2D

    def positions(self) -> Iterator[Vector2D]:
        yield self.origin_position
        yield self.origin_position.move(CardinalDirection.EAST)

    def move(self, direction: CardinalDirection) -> "DoubleWidthBox":
        return DoubleWidthBox(self.origin_position.move(direction, y_grows_down=True))

    @staticmethod
    def from_position(position: Vector2D) -> Iterator["DoubleWidthBox"]:
        yield DoubleWidthBox(position)
        yield DoubleWidthBox(position.move(CardinalDirection.WEST))


class WarehouseBoxes:
    def __init__(self, boxes: set[SingleWidthBox | DoubleWidthBox]) -> None:
        self._boxes = boxes

    def box_positions(self) -> Iterator[Vector2D]:
        yield from (box.origin_position for box in self._boxes)

    def double_width(self) -> "WarehouseBoxes":
        new_boxes = {
            DoubleWidthBox(Vector2D(2 * b.origin_position.x, b.origin_position.y))
            for b in self._boxes
        }
        return WarehouseBoxes(new_boxes)

    @staticmethod
    def _box_candidates_at_position(
        position: Vector2D,
    ) -> Iterator[SingleWidthBox | DoubleWidthBox]:
        yield from SingleWidthBox.from_position(position)
        yield from DoubleWidthBox.from_position(position)

    def _box_at(self, position: Vector2D) -> SingleWidthBox | DoubleWidthBox | None:
        for candidate in self._box_candidates_at_position(position):
            if candidate in self._boxes:
                return candidate

    def boxes_in_front(
        self, position: Vector2D, direction: CardinalDirection
    ) -> Iterator[SingleWidthBox | DoubleWidthBox]:
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
        self, boxes: set[SingleWidthBox | DoubleWidthBox], direction: CardinalDirection
    ) -> "WarehouseBoxes":
        new_boxes = self._boxes - boxes | {box.move(direction) for box in boxes}
        return WarehouseBoxes(new_boxes)
