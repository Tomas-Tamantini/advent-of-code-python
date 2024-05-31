from models.common.io import InputReader
from .parser import parse_art_block_rules, parse_art_block
from .fractal_art import FractalArt


def aoc_2017_d21(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 21: Fractal Art ---")
    inital_pattern = parse_art_block(".#./..#/###")
    rules = parse_art_block_rules(input_reader)
    fractal_art = FractalArt(inital_pattern, rules)
    num_iterations = 5
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"Part 1: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )
    num_iterations = 18
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"Part 2: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )
