from models.common.io import IOHandler
from models.common.vectors import CardinalDirection, Vector2D
from .tree_height_map import TreeHeightMap
from math import prod


def _scenic_score(position: Vector2D, tree_height_map: TreeHeightMap) -> int:
    return prod(
        len(set(tree_height_map.visible_trees_from_position(position, direction)))
        for direction in CardinalDirection
    )


def aoc_2022_d8(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 8: Treetop Tree House ---")
    grid = [
        [int(char) for char in line]
        for line in io_handler.input_reader.read_stripped_lines()
    ]
    tree_height_map = TreeHeightMap(grid)
    visible = set()
    for direction in CardinalDirection:
        visible.update(tree_height_map.visible_trees(direction))
    print(f"Part 1: Total visible trees: {len(visible)}")
    best_scenic_score = max(
        _scenic_score(position, tree_height_map)
        for position in tree_height_map.all_positions()
    )
    print(f"Part 2: Best scenic score: {best_scenic_score}")
