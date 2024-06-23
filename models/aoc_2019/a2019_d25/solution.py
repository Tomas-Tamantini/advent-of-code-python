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
        play_msg = ""
    else:
        control = DroidAutomaticControl(DroidInput())
        play_msg = "(SET FLAG --play TO PLAY THE GAME AND CONTROL THE DROID YOURSELF) "
    io_handler.output_writer.log_progress(f"{play_msg}droid looking for password...")
    run_droid_explore_program(instructions, control)
    solution = ProblemSolution(
        problem_id, f"{play_msg}Airlock password is {control.airlock_password}"
    )
    io_handler.output_writer.write_solution(solution)
