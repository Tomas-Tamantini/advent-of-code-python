from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .memory_bank import MemoryBankBalancer


def aoc_2017_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 6, "Memory Reallocation")
    io_handler.output_writer.write_header(problem_id)
    num_blocks = [int(block) for block in io_handler.input_reader.read().split()]
    balancer = MemoryBankBalancer(num_blocks)
    num_redistributions = len(list(balancer.unique_configurations()))
    yield ProblemSolution(
        problem_id,
        f"Number of redistributions: {num_redistributions}",
        part=1,
        result=num_redistributions,
    )

    loop_size = balancer.loop_size()
    yield ProblemSolution(
        problem_id, f"Loop size: {loop_size}", part=2, result=loop_size
    )
