from .xmas_present import XmasPresent


def test_can_iterate_through_side_areas_of_present():
    present = XmasPresent(2, 3, 4)
    assert set(present.side_areas()) == {6, 8, 12}


def test_area_required_to_wrap_present_is_surface_area_plus_smallest_side_area():
    present = XmasPresent(2, 3, 4)
    assert present.area_required_to_wrap() == 58


def test_can_iterate_through_side_perimeters_of_present():
    present = XmasPresent(2, 3, 4)
    assert set(present.side_perimeters()) == {10, 12, 14}


def test_ribbon_required_to_wrap_present_is_smallest_perimeter_plus_volume():
    present = XmasPresent(2, 3, 4)
    assert present.ribbon_required_to_wrap() == 34
