from models.common.io import InputReader
from models.common.vectors import Vector2D, CardinalDirection
from .tree_height_map import TreeHeightMap


def aoc_2022_d8(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 8: Treetop Tree House ---")
    grid = [[int(char) for char in line] for line in input_reader.read_stripped_lines()]
    tree_height_map = TreeHeightMap(grid)
    visible = set()
    for direction in CardinalDirection:
        visible.update(tree_height_map.visible_trees(direction))
    print(f"Total visible trees: {len(visible)}")
