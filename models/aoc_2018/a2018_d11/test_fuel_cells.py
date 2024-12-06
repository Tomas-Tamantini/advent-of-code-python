import pytest

from .fuel_cells import FuelCells


@pytest.mark.parametrize(
    ("x", "y", "grid_serial_number", "expected_value"),
    [
        (2, 4, 8, 4),
        (121, 78, 57, -5),
        (216, 195, 39, 0),
        (100, 152, 71, 4),
    ],
)
def test_fuel_cells_have_their_values_calculated_properly(
    x, y, grid_serial_number, expected_value
):
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    assert cells.power_at(x, y) == expected_value


@pytest.mark.parametrize(
    ("grid_serial_number", "expected_position"),
    [
        (18, (32, 44)),
        (42, (20, 60)),
    ],
)
def test_can_find_3x3_region_with_largest_total_power(
    grid_serial_number, expected_position
):
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    assert (
        cells.position_with_largest_total_power(
            region_width=3,
            region_height=3,
        )
        == expected_position
    )


@pytest.mark.skip(reason="Takes too long")
@pytest.mark.parametrize(
    ("grid_serial_number", "expected_position", "expected_size"),
    [
        (18, (89, 268), 16),
        (42, (231, 250), 12),
    ],
)
def test_can_find_arbitrary_size_square_with_largest_total_power(
    grid_serial_number, expected_position, expected_size
):
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    square = cells.square_with_largest_total_power()
    assert square.coords_top_left == expected_position
    assert square.size == expected_size
