from dataclasses import dataclass


@dataclass(frozen=True)
class BoatRace:
    total_time: int
    record_distance: int
