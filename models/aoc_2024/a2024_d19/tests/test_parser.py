from models.common.io import InputFromString

from ..parser import parse_available_patterns, parse_desired_designs

_FILE_CONTENT = """
                r, wr, b, g, bwu, rb, gb, br

                brwrr
                bggr
                gbbr
                """


def test_parse_available_patterns():
    input_reader = InputFromString(_FILE_CONTENT)
    available_patterns = list(parse_available_patterns(input_reader))
    assert available_patterns == ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]


def test_parse_desired_designs():
    input_reader = InputFromString(_FILE_CONTENT)
    desired_designs = list(parse_desired_designs(input_reader))
    assert desired_designs == ["brwrr", "bggr", "gbbr"]
