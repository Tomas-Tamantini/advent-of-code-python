from math import inf
from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .voronoi import ManhattanVoronoi


def aoc_2018_d6(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2018 - Day 6: Chronal Coordinates ---")
    lines = list(io_handler.input_reader.readlines())
    coordinates = [Vector2D(*map(int, line.split(","))) for line in lines]
    voronoi = ManhattanVoronoi(coordinates)
    areas = voronoi.areas_after_expansion()
    largest_area = max(a for a in areas.values() if a != inf)
    print(f"Part 1: Largest Voronoi area: {largest_area}")
    num_points = voronoi.num_points_whose_sum_of_distances_is_less_than(
        10000, io_handler.progress_bar
    )
    print(f"Part 2: Number of points: {num_points}")
