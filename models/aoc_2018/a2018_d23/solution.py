from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .nanobot import distance_of_position_with_strongest_signal
from .parser import parse_nanobots


def aoc_2018_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 23, "Experimental Emergency Teleportation")
    io_handler.output_writer.write_header(problem_id)
    bots = list(parse_nanobots(io_handler.input_reader))
    strongest = max(bots, key=lambda b: b.radius)
    num_in_range = sum(strongest.is_in_range(bot.position) for bot in bots)
    yield ProblemSolution(
        problem_id,
        f"Number of bots in range of strongest: {num_in_range}",
        part=1,
        result=num_in_range,
    )

    optimal_distance = distance_of_position_with_strongest_signal(bots)
    yield ProblemSolution(
        problem_id,
        f"Optimal distance from origin with most bots in range: {optimal_distance}",
        part=2,
        result=optimal_distance,
    )
