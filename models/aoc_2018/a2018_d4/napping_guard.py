from collections import defaultdict
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

    def _num_times_asleep_by_minute(self) -> dict[int, int]:
        minutes = defaultdict(int)
        for nap in self.naps:
            for minute in range(nap.start_inclusive.minute, nap.end_exclusive.minute):
                minutes[minute] += 1
        return minutes

    def minute_most_likely_to_be_asleep(self) -> int:
        minutes = self._num_times_asleep_by_minute()
        return max(minutes, key=minutes.get)

    def num_times_slept_on_minute(self, minute: int) -> int:
        return self._num_times_asleep_by_minute()[minute]
