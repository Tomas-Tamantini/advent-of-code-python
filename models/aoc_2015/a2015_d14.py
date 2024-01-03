from dataclasses import dataclass


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
