from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .parser import parse_warehouse, parse_warehouse_robot_moves


def _box_score(box: Vector2D) -> int:
    return box.x + 100 * box.y


def aoc_2024_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 15, "Warehouse Woes")
    io_handler.output_writer.write_header(problem_id)
    warehouse = parse_warehouse(io_handler.input_reader)

    next_warehouse = warehouse
    moves = list(parse_warehouse_robot_moves(io_handler.input_reader))
    for move in moves:
        next_warehouse = next_warehouse.move_robot(move)

    gps_coords = sum(_box_score(b) for b in next_warehouse.box_positions())

    yield ProblemSolution(
        problem_id,
        f"The sum of GPS coordinates is {gps_coords}",
        result=gps_coords,
        part=1,
    )

    next_warehouse = warehouse.double_width()
    for move in moves:
        next_warehouse = next_warehouse.move_robot(move)

    gps_coords = sum(_box_score(b) for b in next_warehouse.box_positions())
    yield ProblemSolution(
        problem_id,
        f"The sum of GPS coordinates for double width warehouse is {gps_coords}",
        result=gps_coords,
        part=2,
    )
