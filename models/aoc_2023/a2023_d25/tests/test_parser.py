from models.common.io import InputFromString

from ..parser import parse_wiring_diagram


def test_parse_wiring_diagram():
    file_content = """aa: bb cc
                      bb: dd"""
    input_reader = InputFromString(file_content)
    graph = parse_wiring_diagram(input_reader)
    assert set(graph.nodes()) == {"aa", "bb", "cc", "dd"}
    assert set(graph.neighbors("bb")) == {"aa", "dd"}
