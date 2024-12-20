from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import BoundingBox

from .parser import parse_positions_and_fold_instructions


def aoc_2021_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 13, "Transparent Origami")
    io_handler.output_writer.write_header(problem_id)
    positions, instructions = parse_positions_and_fold_instructions(
        io_handler.input_reader
    )
    visible_dots = instructions[0].apply(set(positions))
    num_visible_dots = len(visible_dots)
    yield ProblemSolution(
        problem_id,
        f"The number of visible dots after the first fold is {num_visible_dots}",
        part=1,
        result=num_visible_dots,
    )

    for remaining_instructions in instructions[1:]:
        visible_dots = remaining_instructions.apply(visible_dots)

    bounding_box = BoundingBox.from_points(visible_dots)
    matrix = [[" "] * (bounding_box.width + 1) for _ in range(bounding_box.height + 1)]
    for dot in visible_dots:
        matrix[dot.y][dot.x] = "#"
    code = "\n".join("".join(row) for row in matrix)
    yield ProblemSolution(
        problem_id, f"The code after all folds is\n\n{code}\n", part=2, result=code
    )
