from models.common.io import IOHandler
from .lantern_fish import LanternFish, lantern_fish_population_after_n_days


def aoc_2021_d6(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2021, 6, "Lanternfish")
    days_until_reproduction = [
        int(day) for day in io_handler.input_reader.read().split(",")
    ]
    fish_school = [
        LanternFish(days_until_reproduction=days) for days in days_until_reproduction
    ]
    pop_80 = lantern_fish_population_after_n_days(fish_school, days=80)
    print(f"Part 1: The population of lanternfish after 80 days is {pop_80}")
    pop_256 = lantern_fish_population_after_n_days(fish_school, days=256)
    print(f"Part 2: The population of lanternfish after 256 days is {pop_256}")
