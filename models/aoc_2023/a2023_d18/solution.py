from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .dig_plan import DiggerInstruction, DigPlan
from .parser import parse_dig_plan


def _lava_lagoon_area(instructions: Iterator[DiggerInstruction]) -> int:
    dig_plan = DigPlan(list(instructions))
    return dig_plan.dig_area()


def aoc_2023_d18(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 18, "Lavaduct Lagoon")
    io_handler.output_writer.write_header(problem_id)

    area_no_hexa = _lava_lagoon_area(
        parse_dig_plan(io_handler.input_reader, parse_hexadecimal=False)
    )
    yield ProblemSolution(
        problem_id,
        f"The lava pool area ignoring hexadecimal instructions is {area_no_hexa}",
        result=area_no_hexa,
        part=1,
    )

    area_hexa = _lava_lagoon_area(
        parse_dig_plan(io_handler.input_reader, parse_hexadecimal=True)
    )
    yield ProblemSolution(
        problem_id,
        f"The lava pool area considering hexadecimal instructions is {area_hexa}",
        result=area_hexa,
        part=2,
    )
