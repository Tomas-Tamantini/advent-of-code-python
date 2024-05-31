from models.common.io import InputReader
from .parser import parse_triangle_sides


def is_valid_triangle(side_a: int, side_b: int, side_c: int) -> bool:
    return (
        side_a + side_b > side_c
        and side_a + side_c > side_b
        and side_b + side_c > side_a
    )


def aoc_2016_d3(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 3: Squares With Three Sides ---")
    valid_triangles_horizontal = sum(
        is_valid_triangle(*sides)
        for sides in parse_triangle_sides(input_reader, read_horizontally=True)
    )
    valid_triangles_vertical = sum(
        is_valid_triangle(*sides)
        for sides in parse_triangle_sides(input_reader, read_horizontally=False)
    )

    print(
        f"Part 1: Number of valid triangles read horizontally: {valid_triangles_horizontal}"
    )
    print(
        f"Part 2: Number of valid triangles read vertically: {valid_triangles_vertical}"
    )
