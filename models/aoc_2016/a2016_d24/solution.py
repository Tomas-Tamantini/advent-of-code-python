from models.common.io import IOHandler
from .air_duct import AirDuctMaze


def aoc_2016_d24(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2016 - Day 24: Air Duct Spelunking ---")
    blueprint = list(io_handler.input_reader.readlines())

    maze = AirDuctMaze(blueprint)
    min_steps = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=False
    )
    print(
        f"Part 1: Fewest number of steps to visit all points of interest: {min_steps}"
    )
    min_steps_round_trip = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=True
    )
    print(
        f"Part 2: Fewest number of steps to visit all points of interest and return to origin: {min_steps_round_trip}"
    )
