from models.aoc_2018 import GuardNap, Guard
from datetime import datetime


def test_guard_keeps_track_of_total_time_asleep():
    guard = Guard(
        id=0,
        naps=[
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 0),
                end_exclusive=datetime(1518, 11, 1, 0, 5),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 33),
                end_exclusive=datetime(1518, 11, 1, 0, 34),
            ),
        ],
    )

    assert guard.total_minutes_asleep == 6


def test_guard_keeps_track_of_minute_they_are_most_likely_to_be_asleep():
    guard = Guard(
        id=0,
        naps=[
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 5),
                end_exclusive=datetime(1518, 11, 1, 0, 25),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 1, 0, 30),
                end_exclusive=datetime(1518, 11, 1, 0, 55),
            ),
            GuardNap(
                start_inclusive=datetime(1518, 11, 3, 0, 24),
                end_exclusive=datetime(1518, 11, 3, 0, 29),
            ),
        ],
    )

    assert guard.minute_most_likely_to_be_asleep() == 24
