from models.common.io import InputFromString
from ..parser import parse_directed_graph


def test_parse_directed_graph():
    file_content = """Step C must be finished before step A can begin.
                      Step C must be finished before step F can begin."""
    graph = parse_directed_graph(InputFromString(file_content))
    assert len(list(graph.nodes())) == 3
    assert set(graph.outgoing("C")) == {"A", "F"}
    assert set(graph.incoming("A")) == {"C"}
    assert set(graph.incoming("F")) == {"C"}
