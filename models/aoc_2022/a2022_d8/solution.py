from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import CardinalDirection, Vector2D
from .tree_height_map import TreeHeightMap
from math import prod


def _scenic_score(position: Vector2D, tree_height_map: TreeHeightMap) -> int:
    return prod(
        len(set(tree_height_map.visible_trees_from_position(position, direction)))
        for direction in CardinalDirection
    )


def aoc_2022_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 8, "Treetop Tree House")
    io_handler.output_writer.write_header(problem_id)
    grid = [
        [int(char) for char in line]
        for line in io_handler.input_reader.read_stripped_lines()
    ]
    tree_height_map = TreeHeightMap(grid)
    visible = set()
    for direction in CardinalDirection:
        visible.update(tree_height_map.visible_trees(direction))
    solution = ProblemSolution(
        problem_id, f"Total visible trees: {len(visible)}", part=1
    )
    io_handler.set_solution(solution)
    best_scenic_score = max(
        _scenic_score(position, tree_height_map)
        for position in tree_height_map.all_positions()
    )
    solution = ProblemSolution(
        problem_id, f"Best scenic score: {best_scenic_score}", part=2
    )
    io_handler.set_solution(solution)
