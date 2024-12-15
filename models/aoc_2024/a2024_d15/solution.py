from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_warehouse, parse_warehouse_robot_moves
from models.common.vectors import Vector2D


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

    gps_coords = sum(_box_score(b) for b in next_warehouse.boxes)

    yield ProblemSolution(
        problem_id,
        f"The sum of GPS coordinates is {gps_coords}",
        result=gps_coords,
        part=1,
    )
