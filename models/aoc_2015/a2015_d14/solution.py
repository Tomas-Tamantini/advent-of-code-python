from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_reindeers
from .reindeer import ReindeerOlympics


def aoc_2015_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 14, "Reindeer Olympics")
    io_handler.output_writer.write_header(problem_id)
    reindeers = list(parse_reindeers(io_handler.input_reader))
    race_duration = 2503
    reindeer_olympics = ReindeerOlympics(reindeers)
    max_distance = max(reindeer_olympics.positions_at_time(race_duration))
    yield ProblemSolution(
        problem_id,
        f"Furthest reindeer is at position {max_distance}",
        part=1,
        result=max_distance,
    )

    max_points = max(reindeer_olympics.points_at_time(race_duration))
    yield ProblemSolution(
        problem_id,
        f"Reindeer with most points has {max_points} points",
        part=2,
        result=max_points,
    )
