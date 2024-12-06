from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .hull_painting import Hull, run_hull_painting_program


def aoc_2019_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 11, "Space Police")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    all_black_hull = Hull()
    run_hull_painting_program(instructions, all_black_hull)
    yield ProblemSolution(
        problem_id,
        f"Number of panels painted at least once is {all_black_hull.num_panels_painted_at_least_once}",
        part=1,
        result=all_black_hull.num_panels_painted_at_least_once,
    )

    single_white_hull = Hull()
    single_white_hull.paint_panel(Vector2D(0, 0), paint_white=True)
    run_hull_painting_program(instructions, single_white_hull)
    result = single_white_hull.render()
    yield ProblemSolution(problem_id, f"Hull message is\n\n{result}", result, part=2)
