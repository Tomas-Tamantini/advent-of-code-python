from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.number_theory import Interval

from .logic import MachinePartRange, WorkflowNetwork
from .parser import parse_machine_part_ranges, parse_workflows


def aoc_2023_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 19, "Aplenty")
    io_handler.output_writer.write_header(problem_id)
    workflows = list(parse_workflows(io_handler.input_reader))
    ranges = parse_machine_part_ranges(io_handler.input_reader)
    network = WorkflowNetwork(
        initial_workflow_id="in",
        accept_workflow_id="A",
        reject_workflow_id="R",
        workflows=workflows,
    )

    rating_sum = 0
    for initial_range in ranges:
        for accepted in network.accepted_ranges(initial_range):
            rating_sum += accepted.rating_sum()
    yield ProblemSolution(
        problem_id,
        f"The rating sum for all accepted parts is {rating_sum}",
        result=rating_sum,
        part=1,
    )

    initial_range = MachinePartRange({attr: Interval(1, 4000) for attr in "xmas"})
    num_accepted_range = sum(
        accepted.num_parts() for accepted in network.accepted_ranges(initial_range)
    )
    yield ProblemSolution(
        problem_id,
        f"The number of accepted parts considering ranges is {num_accepted_range}",
        result=num_accepted_range,
        part=2,
    )
