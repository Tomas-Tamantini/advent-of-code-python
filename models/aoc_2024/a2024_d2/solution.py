from typing import Iterator

from models.common.io import InputReader, IOHandler, Problem, ProblemSolution

from .report_safety import report_is_safe


def _parse_reports(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for line in input_reader.read_stripped_lines():
        yield tuple(map(int, line.split()))


def aoc_2024_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 2, "Red-Nosed Reports")
    io_handler.output_writer.write_header(problem_id)
    reports = list(_parse_reports(io_handler.input_reader))
    num_safe_reports_zero_tolerance = sum(
        report_is_safe(report, num_bad_levels_tolerance=0) for report in reports
    )
    yield ProblemSolution(
        problem_id,
        f"The number of safe reports with no error tolerance is {num_safe_reports_zero_tolerance}",
        result=num_safe_reports_zero_tolerance,
        part=1,
    )

    num_safe_reports_one_tolerance = sum(
        report_is_safe(report, num_bad_levels_tolerance=1) for report in reports
    )
    yield ProblemSolution(
        problem_id,
        f"The number of safe reports with one error tolerance is {num_safe_reports_one_tolerance}",
        result=num_safe_reports_one_tolerance,
        part=2,
    )
