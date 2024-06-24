from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_xmas_presents


def aoc_2015_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 2, "I Was Told There Would Be No Math")
    io_handler.output_writer.write_header(problem_id)
    presents = list(parse_xmas_presents(io_handler.input_reader))
    total_area = sum(present.area_required_to_wrap() for present in presents)
    yield ProblemSolution(
        problem_id,
        f"Santa needs {total_area} square feet of wrapping paper",
        part=1,
        result=total_area,
    )

    ribbon_length = sum(present.ribbon_required_to_wrap() for present in presents)
    yield ProblemSolution(
        problem_id,
        f"Santa needs {ribbon_length} feet of ribbon",
        part=2,
        result=ribbon_length,
    )
