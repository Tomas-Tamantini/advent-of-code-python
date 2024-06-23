from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_celestial_bodies


def aoc_2019_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 6, "Universal Orbit Map")
    io_handler.output_writer.write_header(problem_id)
    center_of_mass = parse_celestial_bodies(io_handler.input_reader)
    total_orbits = center_of_mass.count_orbits()
    solution = ProblemSolution(
        problem_id,
        f"Total number of direct and indirect orbits is {total_orbits}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    orbital_distance = center_of_mass.orbital_distance("YOU", "SAN") - 2
    solution = ProblemSolution(
        problem_id,
        f"Minimum number of orbital transfers required is {orbital_distance}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
