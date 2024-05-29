from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Reindeer:
    flight_speed: int
    flight_interval: int
    rest_interval: int

    @property
    def total_interval(self) -> int:
        return self.flight_interval + self.rest_interval

    def position_at_time(self, t: int) -> int:
        distance_per_flight = self.flight_speed * self.flight_interval
        num_flights = t // self.total_interval
        total_distance = distance_per_flight * num_flights
        remaining_time = min(t % self.total_interval, self.flight_interval)
        return total_distance + remaining_time * self.flight_speed


class ReindeerOlympics:
    def __init__(self, reindeers: list[Reindeer]) -> None:
        self._reindeers = reindeers

    def positions_at_time(self, t: int) -> list[int]:
        return [r.position_at_time(t) for r in self._reindeers]

    def _indices_of_leading_reindeers_at_time(self, t: int) -> Iterable[int]:
        positions = self.positions_at_time(t)
        max_pos = max(positions)
        for idx, pos in enumerate(positions):
            if pos == max_pos:
                yield idx

    def points_at_time(self, t: int) -> list[int]:
        points = [0 for _ in self._reindeers]
        for second in range(1, t + 1):
            for idx in self._indices_of_leading_reindeers_at_time(second):
                points[idx] += 1
        return points
