from typing import Iterator
from math import inf
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.number_theory import Interval
from .parser import (
    parse_maps,
    parse_seeds_as_intervals,
    parse_seeds_as_standalone_intervals,
)
from .interval_mapper import CompositeIntervalMapper


def _minimum_output(mapper: CompositeIntervalMapper, seeds: list[Interval]) -> int:
    min_value = inf

    for seed in seeds:
        for outout_interval in mapper.map_interval(seed):
            min_value = min(min_value, outout_interval.min_inclusive)

    return min_value


def aoc_2023_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 5, "If You Give A Seed A Fertilizer")
    io_handler.output_writer.write_header(problem_id)
    mappers = list(parse_maps(io_handler.input_reader))
    mapper = CompositeIntervalMapper(*mappers)

    seeds_as_values = list(parse_seeds_as_standalone_intervals(io_handler.input_reader))

    min_output = _minimum_output(mapper, seeds_as_values)

    yield ProblemSolution(
        problem_id,
        f"Part 1: The lowest location with seeds as values is {min_output}",
        result=min_output,
        part=1,
    )

    seeds_as_intervals = list(parse_seeds_as_intervals(io_handler.input_reader))
    min_output = _minimum_output(mapper, seeds_as_intervals)

    yield ProblemSolution(
        problem_id,
        f"Part 2: The lowest location with seeds as ranges is {min_output}",
        result=min_output,
        part=2,
    )
