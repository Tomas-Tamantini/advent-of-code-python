from typing import Iterator, Optional
from models.vectors import Vector2D, TurnDirection, CardinalDirection
from .vacuum_robot import VacuumRobot, VacuumRobotInstruction
from .path_compression import CompressedPath, compress_vacuum_bot_path


class ScaffoldMap:
    def __init__(self) -> None:
        self._map = [[]]
        self._vacuum_robot = None

    @property
    def vacuum_robot(self) -> VacuumRobot:
        return self._vacuum_robot

    def add_pixel(self, pixel: str) -> None:
        if pixel == "\n":
            self._map.append([])
        else:
            self._map[-1].append(pixel)
            if pixel in "^v<>":
                bot_position = Vector2D(len(self._map[-1]) - 1, len(self._map) - 1)
                bot_direction = {
                    "^": CardinalDirection.NORTH,
                    "v": CardinalDirection.SOUTH,
                    "<": CardinalDirection.WEST,
                    ">": CardinalDirection.EAST,
                }[pixel]
                self._vacuum_robot = VacuumRobot(bot_position, bot_direction)

    def render(self) -> str:
        return "\n".join("".join(line) for line in self._map)

    def _is_scaffold(self, pos: Vector2D) -> bool:
        if (
            pos.x < 0
            or pos.y < 0
            or pos.y >= len(self._map)
            or pos.x >= len(self._map[pos.y])
        ):
            return False
        return self._map[pos.y][pos.x] in "#^v<>"

    def _is_intersection(self, position: Vector2D) -> bool:
        if not self._is_scaffold(position):
            return False
        scaffold_neighbors = [
            neighbor
            for neighbor in position.adjacent_positions()
            if self._is_scaffold(neighbor)
        ]

        return len(scaffold_neighbors) > 2

    def scaffolding_intersections(self) -> Iterator[Vector2D]:
        for y, line in enumerate(self._map):
            for x, _ in enumerate(line):
                position = Vector2D(x, y)
                if self._is_intersection(position):
                    yield position

    def _next_turn_direction(self, robot: VacuumRobot) -> Optional[TurnDirection]:
        candidates = (TurnDirection.LEFT, TurnDirection.RIGHT, TurnDirection.NO_TURN)
        for turn_direction in candidates:
            new_position = robot.new_position(
                VacuumRobotInstruction(turn_direction, steps=1)
            )
            if self._is_scaffold(new_position):
                return turn_direction

    def _next_bot_movement(
        self, robot: VacuumRobot
    ) -> Optional[VacuumRobotInstruction]:
        turn_direction = self._next_turn_direction(robot)
        if turn_direction is None:
            return None
        steps = 1
        while self._is_scaffold(
            robot.new_position(VacuumRobotInstruction(turn_direction, steps + 1))
        ):
            steps += 1

        return VacuumRobotInstruction(turn_direction, steps)

    def path_through_scaffolding(self) -> Iterator[VacuumRobotInstruction]:
        virtual_robot = self._vacuum_robot
        while (instruction := self._next_bot_movement(virtual_robot)) is not None:
            yield instruction
            virtual_robot = virtual_robot.move(instruction)

    def compressed_path_through_scaffolding(
        self, num_subroutines: int
    ) -> CompressedPath:
        instructions = list(self.path_through_scaffolding())
        return compress_vacuum_bot_path(instructions, num_subroutines)
