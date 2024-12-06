from models.common.number_theory import Interval
from models.common.vectors import BoundingBox, Vector2D

from ..logic import (
    DiagonalLineSegment,
    ProximitySensor,
    num_positions_which_cannot_contain_beacon,
    position_which_must_be_beacon,
)


def _example_sensor() -> ProximitySensor:
    return ProximitySensor(
        position=Vector2D(8, 7),
        nearest_beacon=Vector2D(2, 10),
    )


def test_proximity_sensor_indicates_if_position_is_out_of_reach():
    assert _example_sensor().is_out_of_reach(Vector2D(4, 1))
    assert not _example_sensor().is_out_of_reach(Vector2D(4, 2))


def test_interval_which_cannot_be_beacon_is_none_in_row_farther_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=17) is None


def test_interval_which_cannot_be_beacon_is_calculated_properly_in_row_closer_than_nearest_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=9) == Interval(1, 15)


def test_interval_which_cannot_be_beacon_discounts_existing_beacon():
    assert _example_sensor().interval_which_cannot_be_beacon(row=10) == Interval(3, 14)


def test_sensor_has_four_diagonal_boundaries_just_out_of_its_reach():
    boundaries = list(_example_sensor().boundaries())
    assert len(boundaries) == 4
    assert set(boundaries) == {
        DiagonalLineSegment(x_interval=Interval(-2, 8), slope_upwards=True, offset=9),
        DiagonalLineSegment(x_interval=Interval(-2, 8), slope_upwards=False, offset=5),
        DiagonalLineSegment(x_interval=Interval(8, 18), slope_upwards=True, offset=-11),
        DiagonalLineSegment(x_interval=Interval(8, 18), slope_upwards=False, offset=25),
    }


def test_diagonal_line_segments_intersect_in_at_most_one_point():
    line_a = DiagonalLineSegment(
        x_interval=Interval(0, 10), slope_upwards=True, offset=2
    )
    line_b = DiagonalLineSegment(
        x_interval=Interval(3, 9), slope_upwards=False, offset=10
    )
    line_c = DiagonalLineSegment(
        x_interval=Interval(0, 10), slope_upwards=False, offset=9
    )
    line_d = DiagonalLineSegment(
        x_interval=Interval(6, 10), slope_upwards=False, offset=10
    )
    assert line_a.intersection(line_b) == Vector2D(4, 6)
    assert line_a.intersection(line_c) is None
    assert line_a.intersection(line_d) is None


def _example_sensors() -> list[ProximitySensor]:
    return [
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


def test_positions_which_cannot_be_beacon_are_union_of_all_sensors():
    assert (
        num_positions_which_cannot_contain_beacon(row=10, sensors=_example_sensors())
        == 26
    )


def test_position_which_must_be_beacon_is_found_by_elimination():
    search_space = BoundingBox(bottom_left=Vector2D(0, 0), top_right=Vector2D(20, 20))
    sensors = _example_sensors()
    assert position_which_must_be_beacon(search_space, sensors) == Vector2D(14, 11)
