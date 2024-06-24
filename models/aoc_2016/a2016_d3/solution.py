from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_triangle_sides


def is_valid_triangle(side_a: int, side_b: int, side_c: int) -> bool:
    return (
        side_a + side_b > side_c
        and side_a + side_c > side_b
        and side_b + side_c > side_a
    )


def aoc_2016_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 3, "Squares With Three Sides")
    io_handler.output_writer.write_header(problem_id)
    valid_triangles_horizontal = sum(
        is_valid_triangle(*sides)
        for sides in parse_triangle_sides(
            io_handler.input_reader, read_horizontally=True
        )
    )
    valid_triangles_vertical = sum(
        is_valid_triangle(*sides)
        for sides in parse_triangle_sides(
            io_handler.input_reader, read_horizontally=False
        )
    )

    yield ProblemSolution(
        problem_id,
        f"Number of valid triangles read horizontally: {valid_triangles_horizontal}",
        part=1,
        result=valid_triangles_horizontal,
    )

    yield ProblemSolution(
        problem_id,
        f"Number of valid triangles read vertically: {valid_triangles_vertical}",
        part=2,
        result=valid_triangles_vertical,
    )
