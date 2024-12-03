from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import parse_program


def aoc_2024_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 3, "Mull It Over")
    io_handler.output_writer.write_header(problem_id)
    program = io_handler.input_reader.read().strip()
    multiplications = list(parse_program(program))
    total = sum(m.result() for m in multiplications)
    yield ProblemSolution(
        problem_id,
        f"The total of all multiplications in the program is {total}",
        result=total,
        part=1,
    )
