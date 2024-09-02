from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import (
    parse_maps,
    parse_seeds_as_intervals,
    parse_seeds_as_standalone_intervals,
)
from .interval_mapper import CompositeIntervalMapper


def aoc_2023_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 5, "If You Give A Seed A Fertilizer")
    io_handler.output_writer.write_header(problem_id)
    mappers = list(parse_maps(io_handler.input_reader))
    mapper = CompositeIntervalMapper(*mappers)

    seeds_as_standalone_intervals = list(
        parse_seeds_as_standalone_intervals(io_handler.input_reader)
    )

    output_intervals = []

    for seed in seeds_as_standalone_intervals:
        output_intervals.extend(mapper.map_interval(seed))

    min_output = min(interval.min_inclusive for interval in output_intervals)

    yield ProblemSolution(
        problem_id,
        f"Part 1: The lowest location with seeds as values is {min_output}",
        result=min_output,
        part=1,
    )
