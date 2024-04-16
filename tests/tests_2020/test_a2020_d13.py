from models.aoc_2020 import (
    BusSchedule,
    earliest_timestamp_to_match_wait_time_and_index_in_list,
)


def test_bus_departs_at_timestamps_multiple_of_its_id():
    bus = BusSchedule(index_in_list=0, bus_id=7)
    assert bus.wait_time(timestamp=14) == 0
    assert bus.wait_time(timestamp=14_000_003) == 4


def test_earliest_timestap_which_makes_wait_time_match_index_in_list_is_calulated_properly():
    schedules = [
        BusSchedule(index_in_list=0, bus_id=17),
        BusSchedule(index_in_list=2, bus_id=13),
        BusSchedule(index_in_list=3, bus_id=19),
    ]
    assert earliest_timestamp_to_match_wait_time_and_index_in_list(schedules) == 3417


def test_earliest_timestap_which_makes_wait_time_match_index_in_list_is_calulated_efficiently():
    schedules = [
        BusSchedule(index_in_list=0, bus_id=19),
        BusSchedule(index_in_list=9, bus_id=41),
        BusSchedule(index_in_list=19, bus_id=523),
        BusSchedule(index_in_list=36, bus_id=17),
        BusSchedule(index_in_list=37, bus_id=13),
        BusSchedule(index_in_list=48, bus_id=29),
        BusSchedule(index_in_list=50, bus_id=853),
        BusSchedule(index_in_list=56, bus_id=37),
        BusSchedule(index_in_list=73, bus_id=23),
    ]
    assert (
        earliest_timestamp_to_match_wait_time_and_index_in_list(schedules)
        == 210612924879242
    )
