from models.common.io import InputReader, CharacterGrid, render_frame
from .octopus_flash import OctopusesFlashes


def aoc_2021_d11(input_reader: InputReader, animate: bool, **_) -> None:
    print("--- AOC 2021 - Day 11: Dumbo Octopus ---")
    grid = CharacterGrid(input_reader.read())
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    octopuses.multi_step(num_steps=100)
    print(f"Part 1: The number of flashes after 100 steps is {octopuses.num_flashes}")

    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    current_step = 0
    while not octopuses.all_octopuses_flashed_last_step:
        current_step += 1
        octopuses.step()
        if animate:
            frame = octopuses.render() + f"\nStep: {current_step}"
            render_frame(frame, sleep_seconds=0.05)
    animation_msg = "" if animate else " (SET FLAG --animate TO SEE COOL ANIMATION)"
    print(
        f"Part 2:{animation_msg} The number of steps until all octopuses flash is {current_step}"
    )
