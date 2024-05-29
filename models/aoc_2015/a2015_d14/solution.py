from models.common.io import InputReader
from .parser import parse_reindeers
from .reindeer import ReindeerOlympics


def aoc_2015_d14(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 14: Reindeer Olympics ---")
    reindeers = list(parse_reindeers(input_reader))
    race_duration = 2503
    reindeer_olympics = ReindeerOlympics(reindeers)
    max_distance = max(reindeer_olympics.positions_at_time(race_duration))
    print(f"Part 1: Furthest reindeer is at position {max_distance}")
    max_points = max(reindeer_olympics.points_at_time(race_duration))
    print(f"Part 2: Reindeer with most points has {max_points} points")
