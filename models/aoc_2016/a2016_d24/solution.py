from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .air_duct import AirDuctMaze


def aoc_2016_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 24, "Air Duct Spelunking")
    io_handler.output_writer.write_header(problem_id)
    blueprint = list(io_handler.input_reader.readlines())

    maze = AirDuctMaze(blueprint)
    min_steps = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=False
    )
    yield ProblemSolution(
        problem_id,
        f"Fewest number of steps to visit all points of interest: {min_steps}",
        part=1,
        result=min_steps,
    )

    min_steps_round_trip = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=True
    )
    yield ProblemSolution(
        problem_id,
        f"Fewest number of steps to visit all points of interest and return to origin: {min_steps_round_trip}",
        part=2,
        result=min_steps_round_trip,
    )
