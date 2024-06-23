from models.common.io import IOHandler, Problem, ProblemSolution
from .fuel_cells import FuelCells


def aoc_2018_d11(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 11, "Chronal Charge")
    io_handler.output_writer.write_header(problem_id)
    grid_serial_number = int(io_handler.input_reader.read())
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    x, y = cells.position_with_largest_total_power(region_width=3, region_height=3)
    solution = ProblemSolution(
        problem_id, f"Position with largest total power: {x+1},{y+1}", part=1
    )
    io_handler.set_solution(solution)
    square = cells.square_with_largest_total_power(io_handler.progress_bar)
    (x, y), s = square.coords_top_left, square.size
    solution = ProblemSolution(
        problem_id,
        f"Position with largest total power and region size: {x+1},{y+1},{s}",
        part=2,
    )
    io_handler.set_solution(solution)
