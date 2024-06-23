from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_fabric_rectangles
from .fabric_area import FabricArea


def aoc_2018_d3(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 3, "No Matter How You Slice It")
    io_handler.output_writer.write_header(problem_id)
    rectangles = parse_fabric_rectangles(io_handler.input_reader)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    solution = ProblemSolution(
        problem_id,
        f"Number of square inches with multiple claims: {len(conflicting_points)}",
        part=1,
    )
    io_handler.set_solution(solution)
    id_without_overlap = fabric_area.rectangle_without_overlap.id
    solution = ProblemSolution(
        problem_id, f"Id of rectangle without overlap: {id_without_overlap}", part=2
    )
    io_handler.set_solution(solution)
