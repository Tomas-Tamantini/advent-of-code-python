from models.common.io import InputFromString
from ..parser import parse_underwater_cave_connections
from ..underwater_cave import UnderwaterCave


def test_parse_underwater_cave_connections():
    file_content = """start-A
                      start-b
                      A-c
                      A-b
                      b-d
                      A-end
                      b-end"""
    connections = parse_underwater_cave_connections(InputFromString(file_content))
    start = UnderwaterCave(name="start", is_small=True)
    assert connections[start] == {
        UnderwaterCave(name="A", is_small=False),
        UnderwaterCave(name="b", is_small=True),
    }
