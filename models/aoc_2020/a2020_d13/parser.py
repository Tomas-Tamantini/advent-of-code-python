from models.common.io import InputReader

from .bus_schedule import BusSchedule


def parse_bus_schedules_and_current_timestamp(
    input_reader: InputReader,
) -> tuple[list[BusSchedule], int]:
    lines = list(input_reader.readlines())
    current_timestamp = int(lines[0].strip())
    bus_schedules = [
        BusSchedule(index_in_list=i, bus_id=int(bus_id))
        for i, bus_id in enumerate(lines[1].strip().split(","))
        if bus_id != "x"
    ]
    return bus_schedules, current_timestamp
