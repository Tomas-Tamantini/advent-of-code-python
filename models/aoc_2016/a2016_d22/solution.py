from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_storage_nodes


def aoc_2016_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 22, "Grid Computing")
    io_handler.output_writer.write_header(problem_id)
    nodes = list(parse_storage_nodes(io_handler.input_reader))
    viable_pairs = sum(
        node_a.makes_viable_pair(node_b) for node_a in nodes for node_b in nodes
    )
    yield ProblemSolution(
        problem_id,
        f"Number of viable pairs: {viable_pairs}",
        part=1,
        result=viable_pairs,
    )

    # TODO: Implement part 2
    yield ProblemSolution(
        problem_id, "Done by hand (move hole around grid): 227", part=2, result=227
    )
