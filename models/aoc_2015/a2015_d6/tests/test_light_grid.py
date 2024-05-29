from ..light_grid import LightGrid, LightGridRegion


def test_light_grid_starts_with_all_lights_off():
    grid = LightGrid(1, 1)
    assert grid.num_lights_on == 0


def test_can_turn_on_region_of_lights():
    grid = LightGrid(10, 10)
    region = LightGridRegion((5, 3), (7, 8))
    grid.turn_on(region)
    assert grid.num_lights_on == 18


def test_can_turn_off_region_of_lights():
    grid = LightGrid(10, 10)
    region_on = LightGridRegion((5, 3), (7, 8))
    grid.turn_on(region_on)
    region_off = LightGridRegion((6, 4), (8, 7))
    grid.turn_off(region_off)
    assert grid.num_lights_on == 10


def test_can_toggle_region_of_lights():
    grid = LightGrid(10, 10)
    region_on = LightGridRegion((5, 3), (7, 8))
    grid.turn_on(region_on)
    region_toggle = LightGridRegion((6, 4), (8, 7))
    grid.toggle(region_toggle)
    assert grid.num_lights_on == 14


def test_can_increment_brightness_of_a_region_of_lights():
    grid = LightGrid(10, 10)
    assert grid.total_brightness == 0
    region = LightGridRegion((5, 3), (7, 8))
    grid.increase_brightness(region, increase=5)
    assert grid.total_brightness == 90


def test_can_decrement_brightness_of_a_region_of_lights():
    grid = LightGrid(10, 10)
    increase_region = LightGridRegion((0, 0), (9, 9))
    grid.increase_brightness(increase_region, increase=10)
    decrease_region = LightGridRegion((5, 5), (7, 7))
    grid.decrease_brightness(decrease_region, decrease=2)
    assert grid.total_brightness == 982


def test_can_brightness_cannot_be_negative():
    grid = LightGrid(10, 10)
    increase_region = LightGridRegion((0, 0), (5, 5))
    grid.increase_brightness(increase_region, increase=10)
    decrease_region = LightGridRegion((4, 4), (7, 7))
    grid.decrease_brightness(decrease_region, decrease=11)
    assert grid.total_brightness == 320
