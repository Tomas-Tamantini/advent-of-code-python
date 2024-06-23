from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_tunnel_maze


def aoc_2019_d18(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 18, "Many-Worlds Interpretation")
    io_handler.output_writer.write_header(problem_id)
    maze = parse_tunnel_maze(io_handler.input_reader)
    min_dist = maze.shortest_distance_to_all_keys()
    solution = ProblemSolution(
        problem_id,
        f"Minimum distance to collect all keys with one robot is {min_dist}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    maze = parse_tunnel_maze(io_handler.input_reader, split_entrance_four_ways=True)
    min_dist = maze.shortest_distance_to_all_keys()
    solution = ProblemSolution(
        problem_id,
        f"Minimum distance to collect all keys with four robots is {min_dist}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
