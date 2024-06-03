from models.common.io import InputReader


def parse_players_starting_positions(input_reader: InputReader) -> tuple[int, int]:
    lines = list(input_reader.readlines())
    return tuple(int(line.strip().split()[-1]) for line in lines)
