from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from models.common.vectors import CardinalDirection
from .parabolic_dish import ParabolicDish


def aoc_2023_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 14, "Parabolic Reflector Dish")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    dish = ParabolicDish(
        width=grid.width,
        height=grid.height,
        cube_rocks=set(grid.positions_with_value("#")),
    )
    rounded_rocks = set(grid.positions_with_value("O"))

    rolled_north = dish.tilt(rounded_rocks, CardinalDirection.NORTH)
    load_one_tilt = dish.load_from_south_edge(rolled_north)
    yield ProblemSolution(
        problem_id,
        f"The load after one tilt is {load_one_tilt}",
        result=load_one_tilt,
        part=1,
    )

    cycle = (
        CardinalDirection.NORTH,
        CardinalDirection.WEST,
        CardinalDirection.SOUTH,
        CardinalDirection.EAST,
    )
    io_handler.output_writer.give_time_estimation("15s", part=2)
    rolled_cycles = dish.run_cycles(rounded_rocks, cycle, num_cycles=1000000000)
    load_cycle = dish.load_from_south_edge(rolled_cycles)
    yield ProblemSolution(
        problem_id,
        f"The load after 1 billion cycles is {load_cycle}",
        result=load_cycle,
        part=2,
    )
