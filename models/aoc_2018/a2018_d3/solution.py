from models.common.io import IOHandler
from .parser import parse_fabric_rectangles
from .fabric_area import FabricArea


def aoc_2018_d3(io_handler: IOHandler) -> None:
    print("--- AOC 2018 - Day 3: No Matter How You Slice It ---")
    rectangles = parse_fabric_rectangles(io_handler.input_reader)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    print(
        f"Part 1: Number of square inches with multiple claims: {len(conflicting_points)}"
    )
    id_without_overlap = fabric_area.rectangle_without_overlap.id
    print(f"Part 2: Id of rectangle without overlap: {id_without_overlap}")
