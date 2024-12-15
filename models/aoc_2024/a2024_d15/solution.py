from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_warehouse, parse_warehouse_robot_moves


def aoc_2024_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 15, "Warehouse Woes")
    io_handler.output_writer.write_header(problem_id)
    warehouse = parse_warehouse(io_handler.input_reader)

    moves = list(parse_warehouse_robot_moves(io_handler.input_reader))
    for move in moves:
        warehouse = warehouse.move_robot(move)

    gps_coords = 0
    for box in warehouse.boxes:
        gps_coords += box.x + 100 * box.y

    yield ProblemSolution(
        problem_id,
        f"The sum of GPS coordinates is {gps_coords}",
        result=gps_coords,
        part=1,
    )
