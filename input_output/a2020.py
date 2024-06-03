from input_output.file_parser import FileParser
from models.common.io import CharacterGrid, InputReader

from models.aoc_2020 import (
    run_game_console,
    find_and_run_game_console_which_terminates,
    solve_jigsaw,
    aoc_2020_d1,
    aoc_2020_d2,
    aoc_2020_d3,
    aoc_2020_d4,
    aoc_2020_d5,
    aoc_2020_d6,
    aoc_2020_d7,
    aoc_2020_d9,
    aoc_2020_d10,
    aoc_2020_d11,
    aoc_2020_d12,
    aoc_2020_d13,
    aoc_2020_d14,
    aoc_2020_d15,
    aoc_2020_d16,
    aoc_2020_d17,
    aoc_2020_d18,
    aoc_2020_d21,
    aoc_2020_d22,
    aoc_2020_d23,
    aoc_2020_d24,
    aoc_2020_d25,
)


# AOC 2020 - Day 8: Handheld Halting
def aoc_2020_d8(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_game_console_instructions(input_reader))
    accumulator = run_game_console(instructions)
    print(f"Part 1: The accumulator value is {accumulator}")
    accumulator = find_and_run_game_console_which_terminates(instructions)
    print(f"Part 2: The accumulator value in program which terminates is {accumulator}")


# AOC 2020 - Day 19: Monster Messages
def aoc_2020_d19(input_reader: InputReader, parser: FileParser, **_):
    cfg, words = parser.parse_context_free_grammar_and_words(
        input_reader, starting_symbol=0
    )
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 1: Number of valid messages is {num_matching}")

    cfg.add_rule(8, (42, 8))
    cfg.add_rule(11, (42, 11, 31))
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 2: Number of valid messages with loops is {num_matching}")


# AOC 2020 - Day 20: Jurassic Jigsaw
def aoc_2020_d20(input_reader: InputReader, parser: FileParser, **_):
    pieces = list(parser.parse_jigsaw_pieces(input_reader))
    solved_jigsaw = solve_jigsaw(pieces)
    border_pieces = list(solved_jigsaw.border_pieces())
    product = 1
    for piece in border_pieces:
        product *= piece.piece_id
    print(f"Part 1: Product of corner pieces is {product}")
    sea_monster_text = "\n".join(
        [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        ]
    )
    sea_monster = CharacterGrid(text=sea_monster_text.replace(" ", "."))
    monster_positions = set(sea_monster.positions_with_value("#"))
    matches = list(solved_jigsaw.find_pattern_matches(monster_positions))
    num_sea_monster_cells = len(monster_positions) * len(matches)
    num_hash_cells = sum(
        1 for cell in solved_jigsaw.render_as_matrix().flatten() if cell
    )
    num_non_sea_monster_cells = num_hash_cells - num_sea_monster_cells
    print(f"Part 2: Number of non-sea-monster cells is {num_non_sea_monster_cells}")


ALL_2020_SOLUTIONS = (
    aoc_2020_d1,
    aoc_2020_d2,
    aoc_2020_d3,
    aoc_2020_d4,
    aoc_2020_d5,
    aoc_2020_d6,
    aoc_2020_d7,
    aoc_2020_d8,
    aoc_2020_d9,
    aoc_2020_d10,
    aoc_2020_d11,
    aoc_2020_d12,
    aoc_2020_d13,
    aoc_2020_d14,
    aoc_2020_d15,
    aoc_2020_d16,
    aoc_2020_d17,
    aoc_2020_d18,
    aoc_2020_d19,
    aoc_2020_d20,
    aoc_2020_d21,
    aoc_2020_d22,
    aoc_2020_d23,
    aoc_2020_d24,
    aoc_2020_d25,
)
