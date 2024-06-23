from models.common.io import IOHandler, Problem
from .parser import parse_cube_positions
from .logic import total_surface_area, external_surface_area


def aoc_2022_d18(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 18, "Boiling Boulders")
    io_handler.output_writer.write_header(problem_id)
    cubes = set(parse_cube_positions(io_handler.input_reader))
    total_area = total_surface_area(cubes)
    print(f"Part 1: Total surface area of droplet is {total_area}")
    external_area = external_surface_area(cubes)
    print(f"Part 2: External surface area of droplet is {external_area}")
