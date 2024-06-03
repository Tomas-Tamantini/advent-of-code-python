from models.common.io import InputReader
from .parser import parse_bus_schedules_and_current_timestamp
from .bus_schedule import earliest_timestamp_to_match_wait_time_and_index_in_list


def aoc_2020_d13(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 13: Shuttle Search ---")
    bus_schedules, timestap = parse_bus_schedules_and_current_timestamp(input_reader)
    wait_time, bus_id = min(
        (
            bus.wait_time(timestap),
            bus.bus_id,
        )
        for bus in bus_schedules
    )
    print(
        f"Part 1: Bus ID {bus_id} multiplied by wait time {wait_time} is {bus_id * wait_time}"
    )
    earliest_timestamp = earliest_timestamp_to_match_wait_time_and_index_in_list(
        bus_schedules
    )
    print(f"Part 2: Earliest timestamp to match bus schedules is {earliest_timestamp}")
