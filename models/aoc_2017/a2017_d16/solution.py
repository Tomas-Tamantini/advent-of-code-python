from models.common.io import IOHandler
from .parser import parse_string_transformers
from .string_transform import transform_string_multiple_rounds


def aoc_2017_d16(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2017, 16, "Permutation Promenade")
    dance_moves = list(parse_string_transformers(io_handler.input_reader))
    dancers = "abcdefghijklmnop"
    for move in dance_moves:
        dancers = move.transform(dancers)
    print(f"Part 1: Final order of dancers: {dancers}")
    num_dances = 1_000_000_000
    dancers = "abcdefghijklmnop"
    dancers = transform_string_multiple_rounds(dancers, dance_moves, num_dances)
    print(f"Part 2: Final order of dancers after {num_dances} dances: {dancers}")
