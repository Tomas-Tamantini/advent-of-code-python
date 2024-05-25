from models.common.vectors import Vector2D
from models.common.number_theory import Interval
from ..logic import ProximitySensor, num_positions_which_cannot_contain_beacon


def _example_sensor() -> ProximitySensor:
    return ProximitySensor(
        position=Vector2D(8, 7),
        nearest_beacon=Vector2D(2, 10),
    )


def test_interval_which_cannot_be_beacon_is_none_in_row_farther_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=17) is None


def test_interval_which_cannot_be_beacon_is_calculated_properly_in_row_closer_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=9) == Interval(1, 15)


def test_interval_which_cannot_be_beacon_discounts_existing_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=10) == Interval(3, 14)


def test_positions_which_cannot_be_beacon_are_union_of_all_sensors():
    sensors = [
        ProximitySensor(Vector2D(2, 18), Vector2D(-2, 15)),
        ProximitySensor(Vector2D(9, 16), Vector2D(10, 16)),
        ProximitySensor(Vector2D(13, 2), Vector2D(15, 3)),
        ProximitySensor(Vector2D(12, 14), Vector2D(10, 16)),
        ProximitySensor(Vector2D(10, 20), Vector2D(10, 16)),
        ProximitySensor(Vector2D(14, 17), Vector2D(10, 16)),
        ProximitySensor(Vector2D(8, 7), Vector2D(2, 10)),
        ProximitySensor(Vector2D(2, 0), Vector2D(2, 10)),
        ProximitySensor(Vector2D(0, 11), Vector2D(2, 10)),
        ProximitySensor(Vector2D(20, 14), Vector2D(25, 17)),
        ProximitySensor(Vector2D(17, 20), Vector2D(21, 22)),
        ProximitySensor(Vector2D(16, 7), Vector2D(15, 3)),
        ProximitySensor(Vector2D(14, 3), Vector2D(15, 3)),
        ProximitySensor(Vector2D(20, 1), Vector2D(15, 3)),
    ]
    assert num_positions_which_cannot_contain_beacon(row=10, sensors=sensors) == 26
