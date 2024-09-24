from dataclasses import dataclass
from math import sqrt, ceil, floor


@dataclass(frozen=True)
class BoatRace:
    total_time: int
    record_distance: int


def number_of_ways_to_beat_boat_race_record(race: BoatRace) -> int:
    delta = race.total_time * race.total_time - 4 * race.record_distance
    if delta <= 0:
        return 0
    sqrt_delta = sqrt(delta)
    root_low = (race.total_time - sqrt_delta) / 2
    root_high = (race.total_time + sqrt_delta) / 2
    lower_bound = floor(root_low) + 1
    upper_bound = ceil(root_high) - 1
    return max(0, upper_bound - lower_bound + 1)
