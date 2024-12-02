from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, InputReader


def _parse_reports(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for line in input_reader.read_stripped_lines():
        yield tuple(map(int, line.split()))


def report_is_safe(report: tuple[int, ...]) -> bool:
    if len(report) < 2:
        return True
    sign = report[1] - report[0]
    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        if diff * sign <= 0:
            return False
        if abs(diff) > 3:
            return False
    return True


def aoc_2024_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 2, "Red-Nosed Reports")
    io_handler.output_writer.write_header(problem_id)
    reports = list(_parse_reports(io_handler.input_reader))
    num_safe_reports = sum(report_is_safe(report) for report in reports)
    yield ProblemSolution(
        problem_id,
        f"The number of safe reports is {num_safe_reports}",
        result=num_safe_reports,
        part=1,
    )
