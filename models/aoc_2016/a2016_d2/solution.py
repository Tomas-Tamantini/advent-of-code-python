from models.common.io import IOHandler
from .parser import parse_cardinal_direction_instructions
from .keypad import Keypad


def aoc_2016_d2(io_handler: IOHandler) -> None:
    print("--- AOC 2016 - Day 2: Bathroom Security ---")
    keypad_three_by_three = Keypad(configuration="123\n456\n789", initial_key="5")
    keypad_rhombus = Keypad(
        configuration="**1**\n*234*\n56789\n*ABC*\n**D**", initial_key="5"
    )
    keys_3x3 = []
    keys_rhombus = []
    for instructions in parse_cardinal_direction_instructions(io_handler.input_reader):
        keypad_three_by_three.move_multiple_keys(instructions)
        keys_3x3.append(keypad_three_by_three.key)
        keypad_rhombus.move_multiple_keys(instructions)
        keys_rhombus.append(keypad_rhombus.key)
    print(f"Part 1: Bathroom code for 3x3 pad is {''.join(keys_3x3)}")
    print(f"Part 2: Bathroom code for rhombus pad is {''.join(keys_rhombus)}")
