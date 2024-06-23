from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import (
    run_droid_explore_program,
    DroidCLIControl,
    DroidAutomaticControl,
    DroidInput,
)


def aoc_2019_d25(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 25, "Cryostasis")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    if io_handler.execution_flags.play:
        control = DroidCLIControl(DroidInput())
    else:
        control = DroidAutomaticControl(DroidInput())
    io_handler.output_writer.log_progress("Droid looking for password...")
    run_droid_explore_program(instructions, control)
    solution = ProblemSolution(
        problem_id,
        f"Airlock password is {control.airlock_password}",
        supports_play=True,
    )
    io_handler.set_solution(solution)
