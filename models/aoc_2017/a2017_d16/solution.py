from models.common.io import InputReader
from .parser import parse_string_transformers
from .string_transform import transform_string_multiple_rounds


def aoc_2017_d16(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 16: Permutation Promenade ---")
    dance_moves = list(parse_string_transformers(input_reader))
    dancers = "abcdefghijklmnop"
    for move in dance_moves:
        dancers = move.transform(dancers)
    print(f"Part 1: Final order of dancers: {dancers}")
    num_dances = 1_000_000_000
    dancers = "abcdefghijklmnop"
    dancers = transform_string_multiple_rounds(dancers, dance_moves, num_dances)
    print(f"Part 2: Final order of dancers after {num_dances} dances: {dancers}")
