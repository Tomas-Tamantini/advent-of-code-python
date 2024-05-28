from .disk_grid import DiskGrid

grid = DiskGrid(key="flqrgnkx", num_rows=128)


def test_grid_calculates_used_squares_for_each_row_from_proper_hash():
    assert grid.get_row(0).startswith("11010100")
    assert grid.get_row(1).startswith("01010101")


def test_grid_calculates_number_of_used_squares():
    assert grid.num_used_squares() == 8108


def test_disk_grid_calculates_number_of_regions_within_itself():
    assert grid.num_regions() == 1242
