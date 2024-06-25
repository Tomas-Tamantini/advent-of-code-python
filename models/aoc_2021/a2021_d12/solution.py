from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_underwater_cave_connections
from .underwater_cave import UnderwaterCaveExplorer


def aoc_2021_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 12, "Passage Pathing")
    io_handler.output_writer.write_header(problem_id)
    connections = parse_underwater_cave_connections(io_handler.input_reader)
    explorer = UnderwaterCaveExplorer(
        connections, start_cave_name="start", end_cave_name="end"
    )
    paths = list(explorer.all_paths())
    yield ProblemSolution(
        problem_id,
        f"The number of paths from start to end is {len(paths)}",
        part=1,
        result=len(paths),
    )

    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    yield ProblemSolution(
        problem_id,
        f"The number of paths from start to end with one small cave visited twice is {len(paths)}",
        part=2,
        result=len(paths),
    )
