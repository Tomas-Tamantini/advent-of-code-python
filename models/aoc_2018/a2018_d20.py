from typing import Iterator
from dataclasses import dataclass
from models.graphs import UndirectedGraph
from models.vectors import Vector2D, CardinalDirection


_str_to_direction = {
    "E": CardinalDirection.EAST,
    "W": CardinalDirection.WEST,
    "N": CardinalDirection.NORTH,
    "S": CardinalDirection.SOUTH,
}


@dataclass(frozen=True)
class _PathToExplore:
    regex: str
    starting_position: Vector2D


def _closing_parenthesis_index(regex: str, opening_parenthesis_idx: int) -> int:
    stack = 0
    for i, char in enumerate(regex[opening_parenthesis_idx + 1 :]):
        if char == "(":
            stack += 1
        elif char == ")":
            if stack == 0:
                return opening_parenthesis_idx + i + 1
            stack -= 1
    raise ValueError("No matching closing parenthesis found")


def _split_options(options: str) -> Iterator[str]:
    stack = 0
    current_option = ""
    for char in options:
        if char == "(":
            stack += 1
        elif char == ")":
            stack -= 1
        elif char == "|" and stack == 0:
            yield current_option
            current_option = ""
            continue
        current_option += char
    yield current_option


def _explore_path(
    graph: UndirectedGraph,
    paths_to_explore: list[_PathToExplore],
    visited: set[_PathToExplore],
) -> None:
    path = paths_to_explore.pop()
    visited.add(path)
    current_position = path.starting_position
    for character in path.regex:
        direction = _str_to_direction.get(character)
        if direction:
            new_position = current_position.move(direction)
            graph.add_edge(current_position, new_position)
            current_position = new_position
        elif character == "(":
            closing_parenthesis_idx = _closing_parenthesis_index(
                path.regex, path.regex.index(character)
            )
            for option in _split_options(
                path.regex[path.regex.index(character) + 1 : closing_parenthesis_idx]
            ):
                new_path = _PathToExplore(
                    option + path.regex[closing_parenthesis_idx + 1 :],
                    current_position,
                )
                if new_path not in visited:
                    paths_to_explore.append(new_path)
            break


def build_lattice_graph(regex: str) -> UndirectedGraph:
    starting_position = Vector2D(0, 0)
    graph = UndirectedGraph()
    graph.add_node(starting_position)
    paths_to_explore = [_PathToExplore(regex[1:], starting_position)]
    visited: set[_PathToExplore] = set()
    while paths_to_explore:
        _explore_path(graph, paths_to_explore, visited)

    return graph
