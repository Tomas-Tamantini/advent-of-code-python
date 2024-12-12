from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import Garden


def aoc_2024_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 12, "Garden Groups")
    io_handler.output_writer.write_header(problem_id)
    garden = Garden(CharacterGrid(io_handler.input_reader.read()))

    dimensions = [r.dimensions() for r in garden.regions()]

    cost_perimeter = sum(d.area * d.perimeter for d in dimensions)
    yield ProblemSolution(
        problem_id,
        f"The cost of the fences considering perimeter is {cost_perimeter}",
        result=cost_perimeter,
        part=1,
    )
