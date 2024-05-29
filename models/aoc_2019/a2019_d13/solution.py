from models.common.io import InputReader
from .arcade import ArcadeGameScreen, run_intcode_arcade, ArcadeGameTile


def aoc_2019_d13(input_reader: InputReader, animate: bool, **_) -> None:
    print("--- AOC 2019 - Day 13: Care Package ---")
    instructions = [int(code) for code in input_reader.read().split(",")]
    screen = ArcadeGameScreen()
    run_intcode_arcade(instructions, screen)
    block_tiles = screen.count_tiles(ArcadeGameTile.BLOCK)
    print(f"Part 1: Number of block tiles is {block_tiles}")
    new_instructions = instructions[:]
    new_instructions[0] = 2
    screen = ArcadeGameScreen(animate=animate)
    animation_msg = (
        "" if animate else " (SET FLAG --animate TO SEE COOL GAME ANIMATION)"
    )
    print(f"Part 2:{animation_msg} simulating game...", end="\r")
    run_intcode_arcade(new_instructions, screen)
    print(f"Part 2:{animation_msg} Final score is {screen.current_score}")