from dataclasses import dataclass
from models.number_theory import ChineseRemainder, solve_chinese_remainder_system


@dataclass(frozen=True)
class BusSchedule:
    index_in_list: int
    bus_id: int

    def wait_time(self, timestamp: int) -> int:
        return (self.bus_id - timestamp) % self.bus_id


def earliest_timestamp_to_match_wait_time_and_index_in_list(
    schedules: list[BusSchedule],
) -> int:
    remainders = [
        ChineseRemainder(
            divisor=bus.bus_id, remainder=(-bus.index_in_list) % bus.bus_id
        )
        for bus in schedules
    ]
    return solve_chinese_remainder_system(*remainders)
