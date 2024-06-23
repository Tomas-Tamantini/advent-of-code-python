from models.common.io import IOHandler
from .parser import parse_celestial_bodies


def aoc_2019_d6(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2019, 6, "Universal Orbit Map")
    center_of_mass = parse_celestial_bodies(io_handler.input_reader)
    total_orbits = center_of_mass.count_orbits()
    print(f"Part 1: Total number of direct and indirect orbits is {total_orbits}")
    orbital_distance = center_of_mass.orbital_distance("YOU", "SAN") - 2
    print(f"Part 2: Minimum number of orbital transfers required is {orbital_distance}")
