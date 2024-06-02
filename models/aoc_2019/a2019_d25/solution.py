from models.common.io import InputReader
from .logic import (
    run_droid_explore_program,
    DroidCLIControl,
    DroidAutomaticControl,
    DroidInput,
)


def aoc_2019_d25(input_reader: InputReader, play: bool, **_) -> None:
    print("--- AOC 2019 - Day 25: Cryostasis ---")
    instructions = [int(code) for code in input_reader.read().split(",")]
    if play:
        control = DroidCLIControl(DroidInput())
        play_msg = ""
    else:
        control = DroidAutomaticControl(DroidInput())
        play_msg = "(SET FLAG --play TO PLAY THE GAME AND CONTROL THE DROID YOURSELF)"
    print(f"{play_msg} droid looking for password...", end="\r")
    run_droid_explore_program(instructions, control)
    print(f"{play_msg} Airlock password is {control.airlock_password}")
