from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_seating_arrangement


def aoc_2015_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 13, "Knights of the Dinner Table")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_seating_arrangement(io_handler.input_reader)
    max_happiness = graph.both_ways_trip_max_cost()
    yield ProblemSolution(
        problem_id,
        f"Maximum happiness without me is {max_happiness}",
        part=1,
        result=max_happiness,
    )

    pre_existing_nodes = list(graph.nodes())
    for n in pre_existing_nodes:
        graph.add_edge("Me", n, 0)
        graph.add_edge(n, "Me", 0)
    max_happiness = graph.both_ways_trip_max_cost()
    yield ProblemSolution(
        problem_id,
        f"Maximum happiness with me is {max_happiness}",
        part=2,
        result=max_happiness,
    )
