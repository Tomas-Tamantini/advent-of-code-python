import pytest

from .fuel_requirement import fuel_requirement


@pytest.mark.parametrize(
    ("rocket_mass", "expected"),
    [
        (2, 0),
        (12, 2),
        (14, 2),
        (1969, 654),
        (100756, 33583),
    ],
)
def test_fuel_requirement_is_calculated_for_mass_of_ship(rocket_mass, expected):
    assert fuel_requirement(rocket_mass, consider_fuel_mass=False) == expected


@pytest.mark.parametrize(
    ("rocket_mass", "expected"),
    [
        (2, 0),
        (12, 2),
        (14, 2),
        (1969, 966),
        (100756, 50346),
    ],
)
def test_fuel_requirement_is_calculated_for_mass_of_ship_and_fuel(
    rocket_mass, expected
):
    assert fuel_requirement(rocket_mass, consider_fuel_mass=True) == expected
