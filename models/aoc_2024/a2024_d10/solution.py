from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import TopographicMap


def aoc_2024_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 10, "Hoof It")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    topographic_map = TopographicMap(grid)
    trails = list(topographic_map.hiking_trails())
    score = len(set(trails))
    yield ProblemSolution(
        problem_id, f"The sum of scores is {score}", result=score, part=1
    )

    rating = len(trails)
    yield ProblemSolution(problem_id, f"The rating is {rating}", result=rating, part=2)
