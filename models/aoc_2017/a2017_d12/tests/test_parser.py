from models.common.io import InputFromString
from ..parser import parse_program_graph


def test_parse_program_graph():
    file_content = """0 <-> 2
                      1 <-> 1
                      2 <-> 0, 3, 4
                      3 <-> 2, 4
                      4 <-> 2, 3, 6
                      5 <-> 6
                      6 <-> 4, 5"""
    graph = parse_program_graph(InputFromString(file_content))
    assert graph.num_nodes == 7
    assert graph.neighbors(1) == {1}
    assert graph.neighbors(2) == {0, 3, 4}
