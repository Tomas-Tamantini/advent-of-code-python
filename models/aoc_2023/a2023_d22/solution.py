from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import BricksDag, drop_bricks
from .parser import parse_bricks


def aoc_2023_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 22, "Sand Slabs")
    io_handler.output_writer.write_header(problem_id)
    bricks = set(parse_bricks(io_handler.input_reader))
    bricks = set(drop_bricks(bricks))
    bricks_dag = BricksDag(bricks)
    topple_chain = {b: set(bricks_dag.bricks_that_would_topple(b)) for b in bricks}
    num_safe_bricks = len([brick for brick, chain in topple_chain.items() if not chain])
    yield ProblemSolution(
        problem_id,
        f"The number of safe bricks to disintegrate is {num_safe_bricks}",
        result=num_safe_bricks,
        part=1,
    )

    num_falling_bricks = sum(len(chain) for chain in topple_chain.values())
    yield ProblemSolution(
        problem_id,
        f"The sum of bricks that would fall is {num_falling_bricks}",
        result=num_falling_bricks,
        part=2,
    )
