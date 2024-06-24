from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_guard_logs


def aoc_2018_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 4, "Repose Record")
    io_handler.output_writer.write_header(problem_id)
    guards = list(parse_guard_logs(io_handler.input_reader))
    guard_most_asleep = max(guards, key=lambda g: g.total_minutes_asleep)
    minute_most_asleep = guard_most_asleep.minute_most_likely_to_be_asleep()
    product = guard_most_asleep.id * minute_most_asleep
    yield ProblemSolution(
        problem_id, f"Guard most asleep has product {product}", part=1
    )

    guard_most_asleep_on_same_minute = max(
        guards,
        key=lambda g: g.num_times_slept_on_minute(g.minute_most_likely_to_be_asleep()),
    )
    minute_most_asleep_on_same_minute = (
        guard_most_asleep_on_same_minute.minute_most_likely_to_be_asleep()
    )
    product = guard_most_asleep_on_same_minute.id * minute_most_asleep_on_same_minute
    yield ProblemSolution(
        problem_id, f"Guard most asleep on same minute has product {product}", part=2
    )
