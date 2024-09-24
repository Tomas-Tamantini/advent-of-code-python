from models.common.io import InputFromString
from ..parser import parse_boat_races
from ..boat_race import BoatRace


def test_boat_races_are_all_parsed_if_considering_white_spaces():
    file_content = """
    Time:      7  15   30
    Distance:  9  40  200"""
    input_reader = InputFromString(file_content)
    races = tuple(parse_boat_races(input_reader, consider_white_spaces=True))
    assert races == (
        BoatRace(total_time=7, record_distance=9),
        BoatRace(total_time=15, record_distance=40),
        BoatRace(total_time=30, record_distance=200),
    )


def test_single_boat_race_is_parsed_if_ignoring_white_spaces():
    file_content = """
    Time:      7  15   30
    Distance:  9  40  200"""
    input_reader = InputFromString(file_content)
    races = tuple(parse_boat_races(input_reader, consider_white_spaces=False))
    assert races == (BoatRace(total_time=71530, record_distance=940200),)
