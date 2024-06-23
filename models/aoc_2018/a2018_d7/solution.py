from models.common.io import IOHandler, Problem
from models.common.graphs import topological_sorting
from .parser import parse_directed_graph
from .jobshop import time_to_complete_jobs


def aoc_2018_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 7, "The Sum of Its Parts")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_directed_graph(io_handler.input_reader)
    order = "".join(topological_sorting(graph, tie_breaker=lambda a, b: a < b))
    print(f"Part 1: Order of steps: {order}")
    time = time_to_complete_jobs(
        num_workers=5,
        jobs_dag=graph,
        job_durations={node: ord(node) - ord("A") + 61 for node in graph.nodes()},
    )
    print(f"Part 2: Time to complete jobs: {time}")
