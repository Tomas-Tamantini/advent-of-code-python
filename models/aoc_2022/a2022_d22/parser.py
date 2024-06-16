from typing import Iterator
from models.common.vectors import Vector2D, TurnDirection
from models.common.io import InputReader
from .logic import (
    CubeNet,
    TurnInstruction,
    MoveForwardInstruction,
    BoardInstruction,
    CubeFace,
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


def _parse_cube_net(lines: list[str], edge_length: int) -> CubeNet:
    walls = dict()
    for row_idx, row in enumerate(lines):
        for column_idx, character in enumerate(row):
            if character in ".#":
                cube_face_position = Vector2D(
                    column_idx // edge_length, row_idx // edge_length
                )
                if cube_face_position not in walls:
                    walls[cube_face_position] = set()
                if character == "#":
                    wall_position = Vector2D(
                        column_idx % edge_length, row_idx % edge_length
                    )
                    walls[cube_face_position].add(wall_position)
    cube_faces_planar_positions = {CubeFace(frozenset(v)): k for k, v in walls.items()}
    return CubeNet(edge_length, cube_faces_planar_positions)


def parse_cube_net_and_instructions(
    input_reader: InputReader, edge_length: int
) -> tuple[CubeNet, list[BoardInstruction]]:
    lines = [l for l in input_reader.readlines() if l.strip()]
    cube_net_lines = lines[:-1]
    instruction_line = lines[-1]
    return _parse_cube_net(cube_net_lines, edge_length), list(
        _parse_instructions(instruction_line)
    )
