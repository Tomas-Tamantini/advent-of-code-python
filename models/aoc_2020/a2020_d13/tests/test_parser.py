from models.common.io import InputFromString

from ..bus_schedule import BusSchedule
from ..parser import parse_bus_schedules_and_current_timestamp


def test_parse_bus_schedules_and_current_timestamp():
    file_content = """939
                      7,13,x,x,59,x,31,19"""
    (
        bus_schedules,
        current_timestamp,
    ) = parse_bus_schedules_and_current_timestamp(InputFromString(file_content))
    assert current_timestamp == 939
    assert bus_schedules == [
        BusSchedule(index_in_list=0, bus_id=7),
        BusSchedule(index_in_list=1, bus_id=13),
        BusSchedule(index_in_list=4, bus_id=59),
        BusSchedule(index_in_list=6, bus_id=31),
        BusSchedule(index_in_list=7, bus_id=19),
    ]
