from models.common.io import CharacterGrid, InputReader

from .logic import CpuRacetrack


def parse_racetrack(input_reader: InputReader) -> CpuRacetrack:
    grid = CharacterGrid(input_reader.read())
    start = next(grid.positions_with_value("S"))
    end = next(grid.positions_with_value("E"))
    wall_positions = set(grid.positions_with_value("#"))
    track_positions = set(grid.positions_with_value(".")) | {start, end}
    return CpuRacetrack(start, end, track_positions, wall_positions)
