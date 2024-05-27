from .optimal_fuel_consumption import (
    optimal_linear_fuel_consumption,
    optimal_triangular_fuel_consumption,
)


def test_optimal_linear_fuel_consumption_aligns_crabs_at_median():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert optimal_linear_fuel_consumption(positions) == 37


def test_optimal_linear_fuel_consumption_aligns_crabs_no_more_than_one_away_from_mean():
    positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert optimal_triangular_fuel_consumption(positions) == 168
