from models.common.io import InputReader
from .disc_system import DiscSystem, SpinningDisc


def _parse_spinning_disc(line: str) -> SpinningDisc:
    parts = line.strip().split(" ")
    num_positions = int(parts[3])
    position_at_time_zero = int(parts[-1].replace(".", ""))
    return SpinningDisc(num_positions, position_at_time_zero)


def parse_disc_system(input_reader: InputReader) -> DiscSystem:
    discs = [_parse_spinning_disc(line) for line in input_reader.readlines()]
    return DiscSystem(discs)
