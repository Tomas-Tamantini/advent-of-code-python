from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .smoke_basin import SmokeBasin


def aoc_2021_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 9, "Smoke Basin")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    basin = SmokeBasin(
        heightmap={pos: int(height) for pos, height in grid.tiles.items()}
    )
    risk_level = sum(height + 1 for _, height in basin.local_minima())
    yield ProblemSolution(
        problem_id,
        f"The risk value of the smoke basin is {risk_level}",
        part=1,
        result=risk_level,
    )

    area_sizes = [len(area) for area in basin.areas()]
    three_largest_areas = sorted(area_sizes, reverse=True)[:3]
    result = three_largest_areas[0] * three_largest_areas[1] * three_largest_areas[2]
    yield ProblemSolution(
        problem_id,
        f"The product of the three largest areas is {result}",
        result,
        part=2,
    )
