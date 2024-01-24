from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GuardNap:
    start_inclusive: datetime
    end_exclusive: datetime

    @property
    def duration_minutes(self) -> int:
        return (self.end_exclusive - self.start_inclusive).seconds // 60


@dataclass
class Guard:
    id: int
    naps: list[GuardNap]

    @property
    def total_minutes_asleep(self) -> int:
        return sum(nap.duration_minutes for nap in self.naps)

    def minute_most_likely_to_be_asleep(self) -> int:
        most_likely = -1
        max_count = -1
        minutes = [0] * 60
        for nap in self.naps:
            for minute in range(nap.start_inclusive.minute, nap.end_exclusive.minute):
                minutes[minute] += 1
                if minutes[minute] > max_count:
                    max_count = minutes[minute]
                    most_likely = minute
        return most_likely
