from typing import Iterator

from models.common.io import CharacterGrid

from .logic import Antenna


def parse_antennas(character_grid: CharacterGrid) -> Iterator[Antenna]:
    for pos, char in character_grid.tiles.items():
        if char.isalnum():
            yield Antenna(char, pos)
