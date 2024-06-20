from typing import Iterator
from dataclasses import dataclass
from models.common.vectors import Vector2D, TurnDirection
from models.common.io import InputReader
from .logic import (
    CubeNet,
    TurnInstruction,
    MoveForwardInstruction,
    BoardInstruction,
)


@dataclass
class _ParsedCube:
    wall_positions: set[Vector2D]
    cube_net: CubeNet
    instructions: list[BoardInstruction]


def _parse_wall_positions(lines: list[str]) -> Iterator[Vector2D]:
    for row_idx, row in enumerate(lines):
        for column_idx, character in enumerate(row):
            if character == "#":
                yield Vector2D(column_idx, row_idx)


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


def _parse_cube_net(lines: list[str], edge_length: int) -> CubeNet:
    face_planar_positions = set()
    for row_idx, row in enumerate(lines):
        for column_idx, character in enumerate(row):
            if character in ".#":
                face_planar_positions.add(
                    Vector2D(column_idx // edge_length, row_idx // edge_length)
                )
    return CubeNet(face_planar_positions)


def parse_cube_net_and_instructions(
    input_reader: InputReader, edge_length: int
) -> _ParsedCube:
    lines = [l for l in input_reader.readlines() if l.strip()]
    cube_net_lines = lines[:-1]
    instruction_line = lines[-1]
    return _ParsedCube(
        wall_positions=set(_parse_wall_positions(cube_net_lines)),
        cube_net=_parse_cube_net(cube_net_lines, edge_length),
        instructions=list(_parse_instructions(instruction_line)),
    )
