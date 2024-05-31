from models.common.io import InputFromString
from ..parser import parse_chip_factory


def test_parse_chip_factory():
    file_content = """value 5 goes to bot 2
                      bot 2 gives low to bot 1 and high to bot 0
                      value 3 goes to bot 1
                      bot 1 gives low to output 1 and high to bot 0
                      bot 0 gives low to output 2 and high to output 0
                      value 2 goes to bot 2"""
    factory = parse_chip_factory(InputFromString(file_content))
    factory.run()
    assert factory.output_bins == {0: [5], 1: [2], 2: [3]}
