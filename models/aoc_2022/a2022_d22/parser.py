from typing import Iterator
from models.common.vectors import Vector2D, TurnDirection
from models.common.io import InputReader
from models.common.number_theory import Interval
from .logic import (
    ObstacleBoard,
    TurnInstruction,
    MoveForwardInstruction,
    BoardInstruction,
)


def _parse_instructions(line: str) -> Iterator[BoardInstruction]:
    num_steps = 0
    for character in line.strip():
        if character.isdigit():
            num_steps = num_steps * 10 + int(character)
        else:
            if num_steps > 0:
                yield MoveForwardInstruction(num_steps)
                num_steps = 0
            if character == "R":
                yield TurnInstruction(TurnDirection.RIGHT)
            elif character == "L":
                yield TurnInstruction(TurnDirection.LEFT)
    if num_steps > 0:
        yield MoveForwardInstruction(num_steps)


def _non_empty_interval(line: str) -> Interval:
    start = 0
    end = len(line)
    while start < len(line) and line[start] not in "#.":
        start += 1
    while end > start and line[end - 1] not in "#.":
        end -= 1
    return Interval(start, end - 1)


def _character_positions(line: str, character: chr) -> Iterator[int]:
    return (idx for idx, c in enumerate(line) if c == character)


def _parse_board(lines: list[str]) -> ObstacleBoard:
    wall_positions = set()
    rows = list()
    for row_idx, line in enumerate(lines):
        rows.append(_non_empty_interval(line))
        for col_idx in _character_positions(line, "#"):
            wall_positions.add(Vector2D(col_idx, row_idx))
    return ObstacleBoard(tuple(rows), wall_positions)


def parse_obstacle_board_and_instructions(
    input_reader: InputReader,
) -> tuple[ObstacleBoard, list[BoardInstruction]]:
    lines = [l for l in input_reader.readlines() if l.strip()]
    board_lines = lines[:-1]
    instruction_line = lines[-1]
    return _parse_board(board_lines), list(_parse_instructions(instruction_line))
