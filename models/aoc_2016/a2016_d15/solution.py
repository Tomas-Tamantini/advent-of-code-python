from models.common.io import IOHandler
from .parser import parse_disc_system
from .disc_system import SpinningDisc


def aoc_2016_d15(io_handler: IOHandler) -> None:
    print("--- AOC 2016 - Day 15: Timing is Everything ---")
    disc_system = parse_disc_system(io_handler.input_reader)
    time_without_extra_disc = disc_system.time_to_press_button()
    print(f"Part 1: Time to press button without extra disc: {time_without_extra_disc}")
    disc_system.add_disc(SpinningDisc(num_positions=11, position_at_time_zero=0))
    time_with_extra_disc = disc_system.time_to_press_button()
    print(f"Part 2: Time to press button with extra disc: {time_with_extra_disc}")
