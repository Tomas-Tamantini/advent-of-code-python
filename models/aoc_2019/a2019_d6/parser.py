from models.common.io import InputReader
from .celestial_body import CelestialBody


def parse_celestial_bodies(input_reader: InputReader) -> CelestialBody:
    bodies = dict()
    for line in input_reader.readlines():
        parts = line.strip().split(")")
        parent = parts[0]
        child = parts[1]
        if parent not in bodies:
            bodies[parent] = CelestialBody(parent)
        if child not in bodies:
            bodies[child] = CelestialBody(child)
        bodies[parent].add_satellite(bodies[child])
    return bodies["COM"]
