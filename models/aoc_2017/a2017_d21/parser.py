import numpy as np
from models.common.io import InputReader
from .fractal_art import ArtBlock


def parse_art_block(block: str) -> ArtBlock:
    return ArtBlock(
        np.array(
            [[1 if c == "#" else 0 for c in line.strip()] for line in block.split("/")]
        )
    )


def parse_art_block_rules(input_reader: InputReader) -> dict[ArtBlock, ArtBlock]:
    rules = {}
    for line in input_reader.readlines():
        parts = line.strip().split(" => ")
        rules[parse_art_block(parts[0])] = parse_art_block(parts[1])
    return rules
