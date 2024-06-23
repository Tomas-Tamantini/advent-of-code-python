from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from models.common.vectors import Vector2D
from .underwater_cave import UnderwaterCaveMaze


def aoc_2021_d15(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 15, "Chiton")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=1,
    )
    start = Vector2D(0, 0)
    end = Vector2D(grid.width - 1, grid.height - 1)
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    solution = ProblemSolution(
        problem_id, f"The risk level of the optimal path is {risk_level}", part=1
    )
    io_handler.set_solution(solution)

    extension_factor = 5
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=extension_factor,
    )
    end = Vector2D(
        grid.width * extension_factor - 1, grid.height * extension_factor - 1
    )
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    solution = ProblemSolution(
        problem_id,
        f"The risk level of the optimal path in the extended cave is {risk_level}",
        part=2,
    )
    io_handler.set_solution(solution)
