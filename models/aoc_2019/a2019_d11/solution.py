from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from .hull_painting import Hull, run_hull_painting_program


def aoc_2019_d11(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 11, "Space Police")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    all_black_hull = Hull()
    run_hull_painting_program(instructions, all_black_hull)
    solution = ProblemSolution(
        problem_id,
        f"Number of panels painted at least once is {all_black_hull.num_panels_painted_at_least_once}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    single_white_hull = Hull()
    single_white_hull.paint_panel(Vector2D(0, 0), paint_white=True)
    run_hull_painting_program(instructions, single_white_hull)
    solution = ProblemSolution(
        problem_id, f"Hull message is\n\n{single_white_hull.render()}", part=2
    )
    io_handler.output_writer.write_solution(solution)
