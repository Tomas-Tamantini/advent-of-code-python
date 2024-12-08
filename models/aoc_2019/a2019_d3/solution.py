from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_directions
from .twisty_wire import TwistyWire


def aoc_2019_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 3, "Crossed Wires")
    io_handler.output_writer.write_header(problem_id)
    wire_a = TwistyWire()
    wire_b = TwistyWire()
    instructions = list(parse_directions(io_handler.input_reader))
    for direction, length in instructions[0]:
        wire_a.add_segment(direction, length)
    for direction, length in instructions[1]:
        wire_b.add_segment(direction, length)
    intersections = set(wire_a.intersection_points(wire_b))
    closest = min(intersections, key=lambda point: point.manhattan_size)
    yield ProblemSolution(
        problem_id,
        (
            f"Closest intersection distance to the "
            f"central port is {closest.manhattan_size}"
        ),
        part=1,
        result=closest.manhattan_size,
    )

    result = min(
        wire_a.distance_to(point) + wire_b.distance_to(point) for point in intersections
    )
    yield ProblemSolution(
        problem_id,
        f"Shortest combined distance to an intersection is {result}",
        result,
        part=2,
    )
