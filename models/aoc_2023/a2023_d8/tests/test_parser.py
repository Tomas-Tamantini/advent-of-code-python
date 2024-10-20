from models.common.io import InputFromString
from ..parser import parse_network_connections, parse_network_steps
from ..logic import NetworkStep

_FILE_CONTENT = """
                LLR

                AAA = (BBB, BBB)
                BBB = (AAA, ZZZ)
                ZZZ = (ZZZ, ZZZ)
                """


def test_parse_network_steps():
    input_reader = InputFromString(_FILE_CONTENT)
    steps = list(parse_network_steps(input_reader))
    assert steps == [NetworkStep.LEFT, NetworkStep.LEFT, NetworkStep.RIGHT]


def test_parse_network_connections():
    input_reader = InputFromString(_FILE_CONTENT)
    connections = parse_network_connections(input_reader)
    assert connections == {
        "AAA": ("BBB", "BBB"),
        "BBB": ("AAA", "ZZZ"),
        "ZZZ": ("ZZZ", "ZZZ"),
    }
