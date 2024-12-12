from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .garden import Garden


def aoc_2024_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 12, "Garden Groups")
    io_handler.output_writer.write_header(problem_id)
    garden = Garden(CharacterGrid(io_handler.input_reader.read()))

    cost_fences = sum(r.area * r.perimeter for r in garden.regions())
    yield ProblemSolution(
        problem_id,
        f"The cost of the fences is {cost_fences}",
        result=cost_fences,
        part=1,
    )
