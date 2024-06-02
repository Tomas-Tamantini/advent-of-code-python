from collections import defaultdict
from typing import Optional, Iterator
from models.common.io import InputReader
from models.common.vectors import Vector2D, CardinalDirection
from .donut_maze import PortalMaze, RecursiveDonutMaze


def _portal_id(position: Vector2D, lines: list[str]) -> Optional[str]:
    for direction in CardinalDirection:
        neighbor_position = position.move(direction)
        if neighbor_position.y < 0 or neighbor_position.y >= len(lines):
            continue
        neighbor_line = lines[neighbor_position.y]
        if neighbor_position.x < 0 or neighbor_position.x >= len(neighbor_line):
            continue
        neighbor_char = neighbor_line[neighbor_position.x]
        if not neighbor_char.isupper():
            continue
        other_char_position = neighbor_position.move(direction)
        other_char = lines[other_char_position.y][other_char_position.x]
        return (
            neighbor_char + other_char
            if direction in {CardinalDirection.NORTH, CardinalDirection.EAST}
            else other_char + neighbor_char
        )


def _open_passage_tiles(lines: list[str]) -> Iterator[Vector2D]:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                yield Vector2D(x, y)


def parse_portal_maze(input_reader: InputReader) -> PortalMaze:
    portals = defaultdict(list)
    maze = PortalMaze()
    lines = list(input_reader.readlines())
    for position in _open_passage_tiles(lines):
        maze.add_node_and_connect_to_neighbors(position)
        portal_id = _portal_id(position, lines)
        if portal_id == "AA":
            maze.set_entrance(position)
        elif portal_id == "ZZ":
            maze.set_exit(position)
        elif portal_id is not None:
            portals[portal_id].append(position)
    for positions in portals.values():
        maze.add_portal(*positions)

    return maze


def _is_inner_edge_of_donut_maze(position: Vector2D, lines: list[str]) -> bool:
    for direction in CardinalDirection:
        intersected_other_tile = False
        new_position = position.move(direction)
        while (0 <= new_position.y < len(lines)) and (
            0 <= new_position.x < len(lines[new_position.y])
        ):
            character = lines[new_position.y][new_position.x]
            if character in {"#", "."}:
                intersected_other_tile = True
                break
            new_position = new_position.move(direction)
        if not intersected_other_tile:
            return False
    return True


def parse_recursive_donut_maze(input_reader: InputReader) -> RecursiveDonutMaze:
    portals = defaultdict(dict)
    maze = RecursiveDonutMaze()
    lines = list(input_reader.readlines())
    for position in _open_passage_tiles(lines):
        maze.add_node(position)
        portal_id = _portal_id(position, lines)
        if portal_id == "AA":
            maze.set_entrance(position)
        elif portal_id == "ZZ":
            maze.set_exit(position)
        elif portal_id is not None:
            kwarg = (
                "step_up"
                if _is_inner_edge_of_donut_maze(position, lines)
                else "step_down"
            )
            portals[portal_id][kwarg] = position

    for positions in portals.values():
        maze.add_portal(**positions)

    return maze
