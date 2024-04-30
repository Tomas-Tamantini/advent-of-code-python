from models.vectors import Vector2D
from models.aoc_2021 import LineSegment


def test_line_segment_is_horizontal_if_dy_is_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(456, 321))
    assert segment.is_horizontal


def test_line_segment_is_not_horizontal_if_dy_is_not_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(123, 456))
    assert not segment.is_horizontal


def test_line_segment_is_vertical_if_dx_is_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(123, 456))
    assert segment.is_vertical


def test_line_segment_is_not_vertical_if_dx_is_not_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(456, 321))
    assert not segment.is_vertical


def test_non_overlapping_segments_have_empty_intersection():
    segment1 = LineSegment(Vector2D(0, 0), Vector2D(10, 0))
    segment2 = LineSegment(Vector2D(0, 10), Vector2D(10, 10))
    assert set(segment1.intersection(segment2)) == set()


def test_segments_which_meet_at_single_point_have_that_point_as_intersection():
    segment1 = LineSegment(Vector2D(0, 5), Vector2D(10, 5))
    segment2 = LineSegment(Vector2D(4, 10), Vector2D(4, 0))
    assert set(segment1.intersection(segment2)) == {Vector2D(4, 5)}


def test_segments_which_meet_at_multiple_points_have_all_those_points_as_intersection():
    segment1 = LineSegment(Vector2D(0, 5), Vector2D(10, 5))
    segment2 = LineSegment(Vector2D(15, 5), Vector2D(8, 5))
    assert set(segment1.intersection(segment2)) == {
        Vector2D(8, 5),
        Vector2D(9, 5),
        Vector2D(10, 5),
    }
