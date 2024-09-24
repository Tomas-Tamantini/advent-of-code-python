import pytest
from ..boat_race import BoatRace, number_of_ways_to_beat_boat_race_record


@pytest.mark.parametrize(
    "race, number_of_ways",
    [
        (BoatRace(7, 90), 0),
        (BoatRace(7, 9), 4),
        (BoatRace(15, 40), 8),
        (BoatRace(30, 200), 9),
        (BoatRace(71_530, 940_200), 71503),
        (BoatRace(38_677_673, 234_102_711_571_236), 23_654_842),
    ],
)
def test_number_of_ways_to_beat_boat_race_record_calculated_efficiently(
    race, number_of_ways
):
    assert number_of_ways_to_beat_boat_race_record(race) == number_of_ways
