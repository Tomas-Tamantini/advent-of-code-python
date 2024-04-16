from models.aoc_2020 import BusSchedule


def test_bus_departs_at_timestamps_multiple_of_its_id():
    bus = BusSchedule(index_in_list=0, bus_id=7)
    assert bus.wait_time(timestamp=14) == 0
    assert bus.wait_time(timestamp=14_000_003) == 4
