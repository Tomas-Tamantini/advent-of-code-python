from models.common.io import IOHandler
from .parser import parse_xmas_presents


def aoc_2015_d2(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 2: I Was Told There Would Be No Math ---")
    presents = list(parse_xmas_presents(io_handler.input_reader))
    total_area = sum(present.area_required_to_wrap() for present in presents)
    print(f"Part 1: Santa needs {total_area} square feet of wrapping paper")
    ribbon_length = sum(present.ribbon_required_to_wrap() for present in presents)
    print(f"Part 2: Santa needs {ribbon_length} feet of ribbon")
