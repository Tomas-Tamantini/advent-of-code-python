from models.common.io import IOHandler, Problem, ProblemSolution
from .beam_area import BeamArea, run_beam_scanner, square_closest_to_beam_source


def aoc_2019_d19(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 19, "Tractor Beam")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    area = BeamArea(width=50, height=50)
    run_beam_scanner(instructions, area)
    solution = ProblemSolution(
        problem_id,
        f"Number of points attracted to the beam is {area.num_points_attracted_to_beam}",
        part=1,
    )
    io_handler.set_solution(solution)
    square_position = square_closest_to_beam_source(
        side_length=100, instructions=instructions, scanned_area=area
    )
    answer = square_position.x * 10_000 + square_position.y
    solution = ProblemSolution(
        problem_id,
        f"Position of the square closest to the beam source is at {answer}",
        part=2,
    )
    io_handler.set_solution(solution)
