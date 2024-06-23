from models.common.io import IOHandler, Problem, CharacterGrid
from .sea_cucumber import SeaCucumbers, SeaCucumbersHerds


def aoc_2021_d25(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 25, "Sea Cucumber")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    sea_cucumbers = SeaCucumbers(width=grid.width, height=grid.height)
    herds = SeaCucumbersHerds(
        east_facing=set(grid.positions_with_value(">")),
        south_facing=set(grid.positions_with_value("v")),
    )
    num_steps = sea_cucumbers.num_steps_until_halt(herds)
    print(f"The number of steps until the herds stop moving is {num_steps}")
