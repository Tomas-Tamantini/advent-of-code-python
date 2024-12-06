from models.common.number_theory import Interval

from ..interval_mapper import (
    CompositeIntervalMapper,
    IntervalOffset,
    PiecewiseIntervalMapper,
)


def test_piecewise_interval_mapper_maps_interval_to_itself_by_default():
    mapper = PiecewiseIntervalMapper()
    interval = Interval(0, 10)
    assert list(mapper.map_interval(interval)) == [interval]


def test_piecewise_interval_mapper_shifts_interval_by_given_offset():
    offset = IntervalOffset(interval=Interval(-100, 100), offset_value=5)
    mapper = PiecewiseIntervalMapper(offset)
    interval = Interval(0, 10)
    assert list(mapper.map_interval(interval)) == [Interval(5, 15)]


def test_piecewise_interval_mapper_shifts_different_interval_pieces_by_different_offsets():
    offset_a = IntervalOffset(interval=Interval(10, 12), offset_value=100)
    offset_b = IntervalOffset(interval=Interval(30, 34), offset_value=-100)
    offset_c = IntervalOffset(interval=Interval(39, 100), offset_value=1000)
    mapper = PiecewiseIntervalMapper(offset_a, offset_b, offset_c)
    interval = Interval(0, 40)
    shifted = list(mapper.map_interval(interval))
    assert len(shifted) == 6
    assert set(shifted) == {
        Interval(0, 9),
        Interval(110, 112),
        Interval(13, 29),
        Interval(-70, -66),
        Interval(35, 38),
        Interval(1039, 1040),
    }


def test_composite_interval_mapper_maps_interval_to_itself_if_no_submappers():
    mapper = CompositeIntervalMapper()
    interval = Interval(0, 10)
    assert list(mapper.map_interval(interval)) == [interval]


def test_composite_interval_mapper_applies_all_submappers_in_order():
    class MockMapperA:
        def map_interval(self, interval):
            yield Interval(interval.min_inclusive + 10, interval.max_inclusive + 10)
            yield Interval(interval.min_inclusive + 30, interval.max_inclusive + 40)

    class MockMapperB:
        def map_interval(self, interval):
            yield Interval(interval.min_inclusive * 2, interval.max_inclusive * 2)

    mapper = CompositeIntervalMapper(MockMapperA(), MockMapperB())
    interval = Interval(0, 10)
    assert list(mapper.map_interval(interval)) == [
        Interval(20, 40),
        Interval(60, 100),
    ]
