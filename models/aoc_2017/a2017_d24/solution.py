from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_bridge_components
from .bridge_builder import BridgeBuilder


def aoc_2017_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 24, "Electromagnetic Moat")
    io_handler.output_writer.write_header(problem_id)
    components = list(parse_bridge_components(io_handler.input_reader))
    builder = BridgeBuilder(components)
    io_handler.output_writer.give_time_estimation("1min", part=1)
    builder.build()
    yield ProblemSolution(
        problem_id, f"Maximum bridge strength: {builder.max_strength}", part=1
    )

    yield ProblemSolution(
        problem_id,
        f"Maximum strength of longest bridge: {builder.max_strength_of_longest_bridge}",
        part=2,
    )
