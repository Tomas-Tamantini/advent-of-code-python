from models.common.io import IOHandler
from .parser import parse_instructions_with_duration
from .logic import RegisterHistory, SpriteScreen


def aoc_2022_d10(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 10: Cathode-Ray Tube ---")
    rh = RegisterHistory()
    for instruction in parse_instructions_with_duration(io_handler.input_reader):
        rh.run_instruction(instruction)
    strengths = [cycle * rh.value_during_cycle(cycle) for cycle in range(20, 221, 40)]
    print(
        f"Part 1: Sum of strengths at cycles 20, 60, 100, 140, and 180: {sum(strengths)}"
    )
    screen = SpriteScreen(width=40, height=6, sprite_length=3)
    sprite_center_positions = rh.register_values
    print(
        f"Part 2: The message formed by the sprite is\n\n{screen.draw(sprite_center_positions)}\n"
    )
