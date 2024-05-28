from models.common.io import InputReader
from .constellations import num_constellations


def aoc_2018_d25(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 25: Four-Dimensional Adventure ---")
    lines = list(input_reader.readlines())
    points = [tuple(map(int, line.split(","))) for line in lines]
    result = num_constellations(max_distance=3, points=points)
    print(f"Number of constellations: {result}")
