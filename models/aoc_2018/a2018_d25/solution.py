from models.common.io import IOHandler, Problem, ProblemSolution
from .constellations import num_constellations


def aoc_2018_d25(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 25, "Four-Dimensional Adventure")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    points = [tuple(map(int, line.split(","))) for line in lines]
    result = num_constellations(max_distance=3, points=points)
    solution = ProblemSolution(problem_id, f"Number of constellations: {result}")
    io_handler.output_writer.write_solution(solution)
