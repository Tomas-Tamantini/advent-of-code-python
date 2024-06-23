from models.common.io import IOHandler, Problem
from .parser import parse_nanobots
from .nanobot import distance_of_position_with_strongest_signal


def aoc_2018_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 23, "Experimental Emergency Teleportation")
    io_handler.output_writer.write_header(problem_id)
    bots = list(parse_nanobots(io_handler.input_reader))
    strongest = max(bots, key=lambda b: b.radius)
    num_in_range = sum(strongest.is_in_range(bot.position) for bot in bots)
    print(f"Part 1: Number of bots in range of strongest: {num_in_range}")
    optimal_distance = distance_of_position_with_strongest_signal(bots)
    print(
        f"Part 2: Optimal distance from origin with most bots in range: {optimal_distance}"
    )
