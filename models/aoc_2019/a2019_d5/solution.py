from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .air_conditioner import run_air_conditioner_program


def aoc_2019_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 5, "Sunny with a Chance of Asteroids")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    result = run_air_conditioner_program(instructions, air_conditioner_id=1)
    yield ProblemSolution(
        problem_id, f"Diagnostic code for air conditioner 1 is {result}", result, part=1
    )

    result = run_air_conditioner_program(instructions, air_conditioner_id=5)
    yield ProblemSolution(
        problem_id, f"Diagnostic code for air conditioner 5 is {result}", result, part=2
    )
