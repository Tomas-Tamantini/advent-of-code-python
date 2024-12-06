from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .fabric_area import FabricArea
from .parser import parse_fabric_rectangles


def aoc_2018_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 3, "No Matter How You Slice It")
    io_handler.output_writer.write_header(problem_id)
    rectangles = parse_fabric_rectangles(io_handler.input_reader)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    yield ProblemSolution(
        problem_id,
        f"Number of square inches with multiple claims: {len(conflicting_points)}",
        part=1,
        result=len(conflicting_points),
    )

    id_without_overlap = fabric_area.rectangle_without_overlap.id
    yield ProblemSolution(
        problem_id,
        f"Id of rectangle without overlap: {id_without_overlap}",
        part=2,
        result=id_without_overlap,
    )
