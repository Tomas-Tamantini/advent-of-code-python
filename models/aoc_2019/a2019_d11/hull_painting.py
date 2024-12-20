from dataclasses import dataclass

from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program
from models.common.vectors import (
    BoundingBox,
    CardinalDirection,
    TurnDirection,
    Vector2D,
)


class Hull:
    def __init__(self) -> None:
        self._white_panels = set()
        self._painted_at_least_once = set()

    @property
    def white_panels(self) -> set[Vector2D]:
        return self._white_panels

    @property
    def num_panels_painted_at_least_once(self) -> int:
        return len(self._painted_at_least_once)

    def is_white(self, position: Vector2D) -> bool:
        return position in self._white_panels

    def paint_panel(self, position: Vector2D, paint_white: bool) -> None:
        self._painted_at_least_once.add(position)
        if paint_white:
            self._white_panels.add(position)
        else:
            self._white_panels.discard(position)

    def render(self) -> str:
        bounding_box = BoundingBox.from_points(self._white_panels)
        result = ""
        for y in reversed(range(bounding_box.min_y, bounding_box.max_y + 1)):
            for x in range(bounding_box.min_x, bounding_box.max_x + 1):
                position = Vector2D(x, y)
                result += "#" if position in self._white_panels else " "
            result += "\n"
        return result


@dataclass
class HullRobot:
    position: Vector2D
    direction: CardinalDirection

    def paint_panel(self, hull: Hull, paint_white: bool) -> None:
        hull.paint_panel(self.position, paint_white)

    def turn_and_move(self, turn_direction: TurnDirection) -> None:
        self.direction = self.direction.turn(turn_direction)
        self.position = self.position.move(self.direction)


class HullRobotIO:
    def __init__(self, hull: Hull, robot: HullRobot) -> None:
        self._hull = hull
        self._robot = robot
        self._output_is_color = True

    def read(self) -> int:
        return 1 if self._hull.is_white(self._robot.position) else 0

    def write(self, value: int) -> None:
        if self._output_is_color:
            self._robot.paint_panel(self._hull, paint_white=value == 1)
        else:
            turn_direction = TurnDirection.LEFT if value == 0 else TurnDirection.RIGHT
            self._robot.turn_and_move(turn_direction)
        self._output_is_color = not self._output_is_color


def run_hull_painting_program(instructions: list[int], hull: Hull) -> None:
    program = IntcodeProgram(instructions)
    robot = HullRobot(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    io = HullRobotIO(hull, robot)
    run_intcode_program(program, serial_input=io, serial_output=io)
