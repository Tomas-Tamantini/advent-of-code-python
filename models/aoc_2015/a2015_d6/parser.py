from models.common.io import InputReader

from .light_grid import LightGrid, LightGridRegion


def _parse_and_give_light_grid_instruction(
    instruction: str, grid: LightGrid, use_elvish_tongue: bool
) -> None:
    parts = instruction.strip().split(" ")
    region = LightGridRegion(
        tuple(map(int, parts[-3].split(","))),
        tuple(map(int, parts[-1].split(","))),
    )
    if "on" in instruction:
        if use_elvish_tongue:
            grid.increase_brightness(region, increase=1)
        else:
            grid.turn_on(region)
    elif "off" in instruction:
        if use_elvish_tongue:
            grid.decrease_brightness(region, decrease=1)
        else:
            grid.turn_off(region)
    else:
        if use_elvish_tongue:
            grid.increase_brightness(region, increase=2)
        else:
            grid.toggle(region)


def parse_and_give_light_grid_instructions(
    input_reader: InputReader, grid: LightGrid, use_elvish_tongue: bool = False
) -> None:
    for line in input_reader.read_stripped_lines():
        _parse_and_give_light_grid_instruction(line, grid, use_elvish_tongue)
