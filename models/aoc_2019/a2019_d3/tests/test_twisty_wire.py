from models.common.vectors import CardinalDirection, Vector2D
from ..twisty_wire import WireSegment, TwistyWire


def test_wire_segment_ends_at_proper_place():
    wire = WireSegment(
        starting_point=Vector2D(0, 0), direction=CardinalDirection.EAST, length=5
    )
    assert wire.ending_point == Vector2D(5, 0)


def test_two_wire_segments_can_have_no_intersection_points():
    wire_a = WireSegment(
        starting_point=Vector2D(0, 0), direction=CardinalDirection.EAST, length=5
    )
    wire_b = WireSegment(
        starting_point=Vector2D(0, 1), direction=CardinalDirection.WEST, length=5
    )
    assert set(wire_a.intersection_points(wire_b)) == set()


def test_two_wire_segments_can_have_single_intersection_point():
    wire_a = WireSegment(
        starting_point=Vector2D(0, 0), direction=CardinalDirection.EAST, length=5
    )
    wire_b = WireSegment(
        starting_point=Vector2D(3, 2), direction=CardinalDirection.SOUTH, length=15
    )
    assert set(wire_a.intersection_points(wire_b)) == {Vector2D(3, 0)}


def test_two_wire_segments_can_have_multiple_intersection_points():
    wire_a = WireSegment(
        starting_point=Vector2D(0, 0), direction=CardinalDirection.EAST, length=5
    )
    wire_b = WireSegment(
        starting_point=Vector2D(4, 0), direction=CardinalDirection.EAST, length=15
    )
    assert set(wire_a.intersection_points(wire_b)) == {
        Vector2D(4, 0),
        Vector2D(5, 0),
    }


def test_twisty_wire_starts_at_origin_without_any_segments():
    wire = TwistyWire()
    assert wire.current_end == Vector2D(0, 0)


def test_can_append_wire_segment_to_twisty_wire():
    wire = TwistyWire()
    wire.add_segment(CardinalDirection.EAST, 5)
    assert wire.current_end == Vector2D(5, 0)


def test_wire_segment_gets_appended_to_the_end_of_previous_wire_segment():
    wire = TwistyWire()
    wire.add_segment(CardinalDirection.EAST, 5)
    wire.add_segment(CardinalDirection.NORTH, 3)
    assert wire.current_end == Vector2D(5, 3)


def test_if_wire_does_not_reach_point_its_distance_is_infinity():
    wire = TwistyWire()
    wire.add_segment(CardinalDirection.EAST, 5)
    wire.add_segment(CardinalDirection.NORTH, 3)
    assert wire.distance_to(Vector2D(100, 100)) == float("inf")


def test_if_wire_reaches_a_point_its_distance_is_first_time_it_reaches():
    wire = TwistyWire()
    wire.add_segment(CardinalDirection.EAST, 8)
    wire.add_segment(CardinalDirection.NORTH, 5)
    wire.add_segment(CardinalDirection.WEST, 5)
    wire.add_segment(CardinalDirection.SOUTH, 3)
    assert wire.distance_to(Vector2D(6, 5)) == 15


def test_can_find_intersection_points_between_two_twisty_wires():
    wire_a = TwistyWire()
    wire_a.add_segment(CardinalDirection.EAST, 8)
    wire_a.add_segment(CardinalDirection.NORTH, 5)
    wire_a.add_segment(CardinalDirection.WEST, 5)
    wire_a.add_segment(CardinalDirection.SOUTH, 3)

    wire_b = TwistyWire()
    wire_b.add_segment(CardinalDirection.NORTH, 7)
    wire_b.add_segment(CardinalDirection.EAST, 6)
    wire_b.add_segment(CardinalDirection.SOUTH, 4)
    wire_b.add_segment(CardinalDirection.WEST, 4)

    assert set(wire_a.intersection_points(wire_b)) == {
        Vector2D(3, 3),
        Vector2D(6, 5),
    }
