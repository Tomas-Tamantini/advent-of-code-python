from typing import Iterator

from models.common.graphs import topological_sorting
from models.common.io import IOHandler, Problem, ProblemSolution

from .jobshop import time_to_complete_jobs
from .parser import parse_directed_graph


def aoc_2018_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 7, "The Sum of Its Parts")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_directed_graph(io_handler.input_reader)
    order = "".join(topological_sorting(graph, tie_breaker=lambda a, b: a < b))
    yield ProblemSolution(problem_id, f"Order of steps: {order}", part=1, result=order)

    time = time_to_complete_jobs(
        num_workers=5,
        jobs_dag=graph,
        job_durations={node: ord(node) - ord("A") + 61 for node in graph.nodes()},
    )
    yield ProblemSolution(
        problem_id, f"Time to complete jobs: {time}", part=2, result=time
    )
