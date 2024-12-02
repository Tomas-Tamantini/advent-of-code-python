from .solution import report_is_safe
import pytest


@pytest.mark.parametrize("good_report", [tuple(), (1,)])
def test_report_with_less_than_two_levels_is_safe(good_report):
    assert report_is_safe(good_report)


@pytest.mark.parametrize("bad_report", [(1, 2, 1), (10, 9, 11, 12)])
def test_report_is_not_safe_if_not_monotonic(bad_report):
    assert not report_is_safe(bad_report)


@pytest.mark.parametrize("bad_report", [(1, 2, 2), (10, 9, 9)])
def test_report_is_not_safe_if_adjacent_levels_differ_by_less_than_one(bad_report):
    assert not report_is_safe(bad_report)


@pytest.mark.parametrize("bad_report", [(1, 2, 6), (10, 9, 5)])
def test_report_is_not_safe_if_adjacent_levels_differ_by_more_than_three(bad_report):
    assert not report_is_safe(bad_report)


@pytest.mark.parametrize("good_report", [(1, 2, 5), (10, 9, 6)])
def test_report_is_safe_if_monotonic_and_adjacent_levels_differ_by_one_to_three(
    good_report,
):
    assert report_is_safe(good_report)
