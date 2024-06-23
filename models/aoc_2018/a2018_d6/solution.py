from math import inf
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from .voronoi import ManhattanVoronoi


def aoc_2018_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 6, "Chronal Coordinates")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    coordinates = [Vector2D(*map(int, line.split(","))) for line in lines]
    voronoi = ManhattanVoronoi(coordinates)
    areas = voronoi.areas_after_expansion()
    largest_area = max(a for a in areas.values() if a != inf)
    solution = ProblemSolution(
        problem_id, f"Largest Voronoi area: {largest_area}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    num_points = voronoi.num_points_whose_sum_of_distances_is_less_than(
        10000, io_handler.progress_bar
    )
    solution = ProblemSolution(problem_id, f"Number of points: {num_points}", part=2)
    io_handler.output_writer.write_solution(solution)
