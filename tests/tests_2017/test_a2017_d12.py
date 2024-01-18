from models.aoc_2017 import ProgramGraph


def test_graph_starts_empty():
    graph = ProgramGraph()
    assert graph.num_nodes == 0


def test_can_add_edges():
    graph = ProgramGraph()
    graph.add_edge(0, 1)
    assert graph.num_nodes == 2


def test_can_query_neighbors():
    graph = ProgramGraph()
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    assert graph.neighbors(0) == {1, 2}
    assert graph.neighbors(1) == {0}
    assert graph.neighbors(2) == {0}
