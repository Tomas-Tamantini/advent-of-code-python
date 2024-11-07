from typing import Iterator
from itertools import combinations
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D, BoundingBox
from .parser import parse_hailstones
from .logic import rays_intersect, rock_that_hits_all_hailstones


def _test_area() -> BoundingBox:
    box_min = 200000000000000
    box_max = 400000000000000
    return BoundingBox(Vector2D(box_min, box_min), Vector2D(box_max, box_max))


def aoc_2023_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 24, "Never Tell Me The Odds")
    io_handler.output_writer.write_header(problem_id)
    hailstones = list(parse_hailstones(io_handler.input_reader))

    test_area = _test_area()
    num_intersections = sum(
        rays_intersect(
            stone_a.xy_plane_projection(), stone_b.xy_plane_projection(), test_area
        )
        for stone_a, stone_b in combinations(hailstones, 2)
    )

    yield ProblemSolution(
        problem_id,
        f"The number of intersections is {num_intersections}",
        result=num_intersections,
        part=1,
    )

    rock = rock_that_hits_all_hailstones(hailstones)
    sum_coords = rock.position.x + rock.position.y + rock.position.z
    yield ProblemSolution(
        problem_id,
        f"The sum of coordinates of the rock's position is {sum_coords}",
        result=sum_coords,
        part=2,
    )
