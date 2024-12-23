from typing import Iterator

from models.common.graphs import UndirectedGraph
from models.common.io import IOHandler, Problem, ProblemSolution

from .cliques import max_clique, three_cliques
from .parser import parse_connections


def aoc_2024_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 23, "LAN Party")
    io_handler.output_writer.write_header(problem_id)
    graph = UndirectedGraph()
    for edge in parse_connections(io_handler.input_reader):
        graph.add_edge(*edge)
    cliques = set(three_cliques(graph))
    num_cliques = 0
    for clique in cliques:
        if any(node.startswith("t") for node in clique):
            num_cliques += 1

    yield ProblemSolution(
        problem_id,
        f"The number of cliques is {num_cliques}",
        result=num_cliques,
        part=1,
    )

    password = ",".join(sorted(max_clique(graph)))

    yield ProblemSolution(
        problem_id, f"The clique password is {password}", result=password, part=2
    )
