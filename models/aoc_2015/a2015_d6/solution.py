from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_and_give_light_grid_instructions
from .light_grid import LightGrid


def aoc_2015_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 6, "Probably a Fire Hazard")
    io_handler.output_writer.write_header(problem_id)
    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(io_handler.input_reader, grid)
    solution = ProblemSolution(
        problem_id,
        f"There are {grid.num_lights_on} lights on",
        part=1,
        result=grid.num_lights_on,
    )
    io_handler.set_solution(solution)
    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(
        io_handler.input_reader, grid, use_elvish_tongue=True
    )
    solution = ProblemSolution(
        problem_id,
        f"The total brightness is {grid.num_lights_on}",
        part=2,
        result=grid.num_lights_on,
    )
    io_handler.set_solution(solution)
