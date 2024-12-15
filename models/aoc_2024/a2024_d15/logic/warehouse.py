from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D

from .warehouse_box import WarehouseBoxes


class Warehouse:
    def __init__(self, robot: Vector2D, boxes: WarehouseBoxes, walls: set[Vector2D]):
        self._robot = robot
        self._boxes = boxes
        self._walls = walls

    @property
    def robot(self) -> Vector2D:
        return self._robot

    def box_positions(self) -> Iterator[Vector2D]:
        yield from self._boxes.box_positions()

    @property
    def walls(self) -> set[Vector2D]:
        return self._walls

    def _box_runs_into_wall(self, box: Vector2D, direction: CardinalDirection) -> bool:
        return set(box.move(direction).positions()) & self._walls

    def move_robot(self, direction: CardinalDirection) -> "Warehouse":
        new_robot = self._robot.move(direction, y_grows_down=True)
        if new_robot in self._walls:
            return self
        boxes_to_move = set()
        for box in self._boxes.boxes_in_front(self._robot, direction):
            if self._box_runs_into_wall(box, direction):
                return self
            else:
                boxes_to_move.add(box)
        new_boxes = self._boxes.move_boxes(boxes_to_move, direction)
        return Warehouse(new_robot, new_boxes, self._walls)
