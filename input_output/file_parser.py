from models.aoc_2015 import XmasPresent, LightGrid, LightGridRegion
from typing import Iterator


def parse_xmas_presents(file_name: str) -> Iterator[XmasPresent]:
    with open(file_name, "r") as f:
        for line in f:
            yield XmasPresent(*map(int, line.split("x")))


def parse_and_give_light_grid_instruction(
    instruction: str, grid: LightGrid, use_elvish_tongue: bool = False
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
