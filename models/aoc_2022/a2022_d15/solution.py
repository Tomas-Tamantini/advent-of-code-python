from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D, BoundingBox
from .parser import parse_proximity_sensors
from .logic import (
    num_positions_which_cannot_contain_beacon,
    position_which_must_be_beacon,
)


def aoc_2022_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 15, "Beacon Exclusion Zone")
    io_handler.output_writer.write_header(problem_id)
    sensors = list(parse_proximity_sensors(io_handler.input_reader))
    num_positions = num_positions_which_cannot_contain_beacon(
        row=2_000_000, sensors=sensors
    )
    yield ProblemSolution(
        problem_id,
        f"Number of positions which cannot contain a beacon is {num_positions}",
        part=1,
        result=num_positions,
    )

    limit = 4_000_000
    search_space = BoundingBox(
        bottom_left=Vector2D(0, 0), top_right=Vector2D(limit, limit)
    )
    position = position_which_must_be_beacon(search_space, sensors)
    result = position.x * limit + position.y
    yield ProblemSolution(
        problem_id, f"Position which must contain a beacon is {result}", result, part=2
    )
