from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from .octopus_flash import OctopusesFlashes


def test_each_octopus_raises_its_energy_level_by_one_after_each_step():
    octopuses = OctopusesFlashes(energy_levels={Vector2D(0, 0): 4, Vector2D(1, 0): 2})
    octopuses.step()
    assert octopuses.energy_levels == {Vector2D(0, 0): 5, Vector2D(1, 0): 3}


def test_an_octopus_which_exceeds_flash_threshold_flashes_and_goes_back_to_zero():
    octopuses = OctopusesFlashes(energy_levels={Vector2D(0, 0): 9}, flash_threshold=9)
    octopuses.step()
    assert octopuses.energy_levels == {Vector2D(0, 0): 0}


def test_an_octopus_which_flashes_increases_energy_level_of_all_neighbors_by_one():
    octopuses = OctopusesFlashes(
        energy_levels={
            Vector2D(0, 0): 9,
            Vector2D(1, 0): 0,
            Vector2D(1, 1): 7,
        }
    )
    octopuses.step()
    assert octopuses.energy_levels == {
        Vector2D(0, 0): 0,
        Vector2D(1, 0): 2,
        Vector2D(1, 1): 9,
    }


def test_octopus_flashes_are_counted_over_many_steps():
    grid = CharacterGrid(
        """5483143223
           2745854711
           5264556173
           6141336146
           6357385478
           4167524645
           2176841721
           6882881134
           4846848554
           5283751526"""
    )
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    octopuses.multi_step(num_steps=100)
    assert octopuses.num_flashes == 1656


def test_octopus_can_all_flashes_at_the_same_time():
    grid = CharacterGrid(
        """767
           686
           767"""
    )
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    assert not octopuses.all_octopuses_flashed_last_step
    octopuses.step()
    assert not octopuses.all_octopuses_flashed_last_step
    octopuses.step()
    assert octopuses.all_octopuses_flashed_last_step


def test_octopuses_flashes_can_be_rendered():
    grid = CharacterGrid(
        """767
           686
           767"""
    )
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    assert octopuses.render() == "767\n686\n767"
