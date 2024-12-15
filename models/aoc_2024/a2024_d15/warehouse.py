from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class Warehouse:
    robot: Vector2D
    boxes: set[Vector2D]
    walls: set[Vector2D]

    def _boxes_in_front(self, direction: CardinalDirection) -> Iterator[Vector2D]:
        current_pos = self.robot.move(direction, y_grows_down=True)
        while current_pos in self.boxes:
            yield current_pos
            current_pos = current_pos.move(direction, y_grows_down=True)

    def move_robot(self, direction: CardinalDirection) -> "Warehouse":
        new_robot = self.robot.move(direction, y_grows_down=True)
        if new_robot in self.walls:
            return self
        boxes_in_front = list(self._boxes_in_front(direction))
        if not boxes_in_front:
            return Warehouse(robot=new_robot, boxes=self.boxes, walls=self.walls)
        else:
            box_to_remove = boxes_in_front[0]
            box_to_add = boxes_in_front[-1].move(direction, y_grows_down=True)
            if box_to_add in self.walls:
                return self
            else:
                new_boxes = self.boxes - {box_to_remove} | {box_to_add}
                return Warehouse(robot=new_robot, boxes=new_boxes, walls=self.walls)
