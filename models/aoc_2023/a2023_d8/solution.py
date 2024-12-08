from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import BinaryNetwork
from .parser import parse_network_connections, parse_network_steps


def aoc_2023_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 8, "Haunted Wasteland")
    io_handler.output_writer.write_header(problem_id)
    connections = parse_network_connections(io_handler.input_reader)
    steps = list(parse_network_steps(io_handler.input_reader))
    network = BinaryNetwork(connections, steps)

    num_steps_single_traveler = network.num_steps_to_finish(
        start_nodes=["AAA"], end_nodes=["ZZZ"]
    )
    yield ProblemSolution(
        problem_id,
        (
            "The number of steps for single traveler to finish is "
            f"{num_steps_single_traveler}"
        ),
        result=num_steps_single_traveler,
        part=1,
    )

    start_nodes = [n for n in connections if n[-1] == "A"]
    end_nodes = [n for n in connections if n[-1] == "Z"]
    num_steps_multiple_travelers = network.num_steps_to_finish(start_nodes, end_nodes)
    yield ProblemSolution(
        problem_id,
        (
            "The number of steps for multiple travelers to finish is "
            f"{num_steps_multiple_travelers}"
        ),
        result=num_steps_multiple_travelers,
        part=2,
    )
