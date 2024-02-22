from math import inf
from typing import Iterator, Optional
from dataclasses import dataclass
from models.vectors import Vector2D, TurnDirection, CardinalDirection
from .intcode import IntcodeProgram, run_intcode_program


@dataclass(frozen=True)
class VacuumRobotInstruction:
    turn: TurnDirection
    steps: int

    def __str__(self) -> str:
        return f"{self.turn.value},{self.steps}"


@dataclass(frozen=True)
class _VacuumRobot:
    position: Vector2D
    direction: CardinalDirection

    def new_position(self, instruction: VacuumRobotInstruction) -> Vector2D:
        new_direction = self.direction.turn(instruction.turn)
        new_position = self.position.move(
            new_direction, num_steps=instruction.steps, y_grows_down=True
        )
        return new_position

    def move(self, instruction: VacuumRobotInstruction) -> "_VacuumRobot":
        new_direction = self.direction.turn(instruction.turn)
        new_position = self.position.move(
            new_direction, num_steps=instruction.steps, y_grows_down=True
        )
        return _VacuumRobot(new_position, new_direction)


class ScaffoldMap:
    def __init__(self) -> None:
        self._map = [[]]
        self._vacuum_robot = None

    @property
    def vacuum_robot(self) -> _VacuumRobot:
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
                self._vacuum_robot = _VacuumRobot(bot_position, bot_direction)

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

    def _next_turn_direction(self) -> Optional[TurnDirection]:
        candidates = (TurnDirection.LEFT, TurnDirection.RIGHT, TurnDirection.NO_TURN)
        for turn_direction in candidates:
            new_position = self._vacuum_robot.new_position(
                VacuumRobotInstruction(turn_direction, steps=1)
            )
            if self._is_scaffold(new_position):
                return turn_direction

    def _next_bot_movement(self) -> Optional[VacuumRobotInstruction]:
        turn_direction = self._next_turn_direction()
        if turn_direction is None:
            return None
        steps = 1
        while self._is_scaffold(
            self._vacuum_robot.new_position(
                VacuumRobotInstruction(turn_direction, steps + 1)
            )
        ):
            steps += 1

        return VacuumRobotInstruction(turn_direction, steps)

    def path_through_scaffolding(self) -> Iterator[VacuumRobotInstruction]:
        while (instruction := self._next_bot_movement()) is not None:
            yield instruction
            self._vacuum_robot = self._vacuum_robot.move(instruction)


@dataclass
class _CompressedPath:
    main_routine: str
    subroutines: dict[str, str]

    @property
    def max_length(self) -> int:
        return max(
            len(self.main_routine),
            max(len(subroutine) for subroutine in self.subroutines.values()),
        )


def compress_vacuum_bot_path(
    instructions: list[VacuumRobotInstruction],
    num_subroutines: int,
) -> _CompressedPath:
    raise NotImplementedError()


class CameraOutput:
    def __init__(self, scaffold_map: ScaffoldMap) -> None:
        self._scaffold_map = scaffold_map

    def write(self, value: int) -> None:
        self._scaffold_map.add_pixel(chr(value))


def run_scaffolding_program(scaffold_map: ScaffoldMap, instructions: list[int]) -> None:
    program = IntcodeProgram(instructions[:])
    camera_output = CameraOutput(scaffold_map)
    run_intcode_program(program, serial_output=camera_output)
