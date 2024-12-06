from models.common.io import InputFromString

from ..fractal_art import FractalArt
from ..parser import parse_art_block, parse_art_block_rules


def test_parse_art_block():
    block = ".#./..#/###"
    art_block = parse_art_block(block)
    assert art_block.num_cells_on == 5


def test_parse_art_block_rules():
    file_content = """../.# => ##./#../...
                      .#./..#/### => #..#/..../..../#..#"""
    rules = parse_art_block_rules(InputFromString(file_content))
    fractal_art = FractalArt(
        initial_pattern=parse_art_block(".#./..#/###"), rules=rules
    )
    assert fractal_art.num_cells_on_after_iterations(2) == 12
