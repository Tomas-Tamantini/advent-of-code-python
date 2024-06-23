from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .smoke_basin import SmokeBasin


def aoc_2021_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 9, "Smoke Basin")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    basin = SmokeBasin(
        heightmap={pos: int(height) for pos, height in grid.tiles.items()}
    )
    risk_level = sum(height + 1 for _, height in basin.local_minima())
    solution = ProblemSolution(
        problem_id, f"The risk value of the smoke basin is {risk_level}", part=1
    )
    io_handler.output_writer.write_solution(solution)

    area_sizes = [len(area) for area in basin.areas()]
    three_largest_areas = sorted(area_sizes, reverse=True)[:3]
    product = three_largest_areas[0] * three_largest_areas[1] * three_largest_areas[2]
    solution = ProblemSolution(
        problem_id, f"The product of the three largest areas is {product}", part=2
    )
    io_handler.output_writer.write_solution(solution)
