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


def test_can_divide_graph_into_disjoint_groups():
    graph = ProgramGraph()
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(3, 5)
    graph.add_edge(6, 6)
    assert list(graph.disjoint_groups()) == [{0, 1, 2}, {3, 4, 5}, {6}]
