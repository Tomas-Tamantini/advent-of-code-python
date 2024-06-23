from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .lumber_area import LumberArea, AcreType


def aoc_2018_d18(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 18, "Settlers of The North Pole")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    area = LumberArea(width=grid.width, height=grid.height)
    cells = grid.tiles
    cells_after_10 = area.multi_step(cells, 10)
    num_wooded = sum(c == AcreType.TREE for c in cells_after_10.values())
    num_lumberyards = sum(c == AcreType.LUMBERYARD for c in cells_after_10.values())
    solution = ProblemSolution(
        problem_id,
        f"Resource value after 10 minutes: {num_wooded * num_lumberyards}",
        part=1,
    )
    io_handler.set_solution(solution)
    io_handler.output_writer.give_time_estimation("1min", part=2)
    cells_after_1b = area.multi_step(cells, 1_000_000_000)
    num_wooded = sum(c == AcreType.TREE for c in cells_after_1b.values())
    num_lumberyards = sum(c == AcreType.LUMBERYARD for c in cells_after_1b.values())
    solution = ProblemSolution(
        problem_id,
        f"Resource value after 1 billion minutes: {num_wooded * num_lumberyards}",
        part=2,
    )
    io_handler.set_solution(solution)
