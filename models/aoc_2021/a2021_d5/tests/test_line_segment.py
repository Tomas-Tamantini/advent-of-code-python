from models.common.vectors import Vector2D

from ..line_segment import LineSegment


def test_line_segment_is_horizontal_if_dy_is_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(456, 321))
    assert segment.is_horizontal
    assert not segment.is_diagonal


def test_line_segment_is_not_horizontal_if_dy_is_not_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(123, 456))
    assert not segment.is_horizontal


def test_line_segment_is_vertical_if_dx_is_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(123, 456))
    assert segment.is_vertical
    assert not segment.is_diagonal


def test_line_segment_is_not_vertical_if_dx_is_not_zero():
    segment = LineSegment(Vector2D(123, 321), Vector2D(456, 321))
    assert not segment.is_vertical


def test_line_segment_is_diagonal_if_not_vertical_or_horizontal():
    segment = LineSegment(Vector2D(123, 321), Vector2D(456, 456))
    assert segment.is_diagonal


def test_horizontal_line_segment_iterates_through_all_its_points():
    segment = LineSegment(Vector2D(123, 321), Vector2D(121, 321))
    points = list(segment.all_points())
    assert points == [Vector2D(123, 321), Vector2D(122, 321), Vector2D(121, 321)]


def test_vertical_line_segment_iterates_through_all_its_points():
    segment = LineSegment(Vector2D(123, 321), Vector2D(123, 323))
    points = list(segment.all_points())
    assert points == [Vector2D(123, 321), Vector2D(123, 322), Vector2D(123, 323)]


def test_diagonal_line_segment_iterates_through_all_its_points():
    segment = LineSegment(Vector2D(0, 3), Vector2D(3, 0))
    points = list(segment.all_points())
    assert points == [
        Vector2D(0, 3),
        Vector2D(1, 2),
        Vector2D(2, 1),
        Vector2D(3, 0),
    ]
