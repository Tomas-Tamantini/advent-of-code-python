from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_disc_system
from .disc_system import SpinningDisc


def aoc_2016_d15(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 15, "Timing is Everything")
    io_handler.output_writer.write_header(problem_id)
    disc_system = parse_disc_system(io_handler.input_reader)
    time_without_extra_disc = disc_system.time_to_press_button()
    solution = ProblemSolution(
        problem_id,
        f"Time to press button without extra disc: {time_without_extra_disc}",
        part=1,
    )
    io_handler.set_solution(solution)
    disc_system.add_disc(SpinningDisc(num_positions=11, position_at_time_zero=0))
    time_with_extra_disc = disc_system.time_to_press_button()
    solution = ProblemSolution(
        problem_id,
        f"Time to press button with extra disc: {time_with_extra_disc}",
        part=2,
    )
    io_handler.set_solution(solution)
