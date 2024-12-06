from typing import Iterable, Iterator

from models.common.io import InputReader

from .boat_race import BoatRace


def _concatenate(numbers: Iterable[int]) -> int:
    return int("".join(map(str, numbers)))


def parse_boat_races(
    input_reader: InputReader, consider_white_spaces: bool
) -> Iterator[BoatRace]:
    times = []
    distances = []
    for line in input_reader.read_stripped_lines():
        if "Time" in line:
            times = list(map(int, line.split(":")[1].split()))
        elif "Distance" in line:
            distances = list(map(int, line.split(":")[1].split()))
    if consider_white_spaces:
        yield from (BoatRace(t, d) for t, d in zip(times, distances))
    else:
        yield BoatRace(_concatenate(times), _concatenate(distances))
