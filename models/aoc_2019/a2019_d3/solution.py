from models.common.io import InputReader
from .parser import parse_directions
from .twisty_wire import TwistyWire


def aoc_2019_d3(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 3: Crossed Wires ---")
    wire_a = TwistyWire()
    wire_b = TwistyWire()
    instructions = list(parse_directions(input_reader))
    for direction, length in instructions[0]:
        wire_a.add_segment(direction, length)
    for direction, length in instructions[1]:
        wire_b.add_segment(direction, length)
    intersections = set(wire_a.intersection_points(wire_b))
    closest = min(intersections, key=lambda point: point.manhattan_size)
    print(
        f"Part 1: Closest intersection distance to the central port is {closest.manhattan_size}"
    )
    shortest = min(
        wire_a.distance_to(point) + wire_b.distance_to(point) for point in intersections
    )
    print(f"Part 2: Shortest combined distance to an intersection is {shortest}")