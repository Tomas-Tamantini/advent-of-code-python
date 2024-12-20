from models.common.io import CharacterGrid, InputReader

from .logic import CpuRacetrack


def parse_racetrack(input_reader: InputReader) -> CpuRacetrack:
    grid = CharacterGrid(input_reader.read())
    return CpuRacetrack(
        start=next(grid.positions_with_value("S")),
        end=next(grid.positions_with_value("E")),
        track_positions=set(grid.positions_with_value(".")),
        wall_positions=set(grid.positions_with_value("#")),
    )
