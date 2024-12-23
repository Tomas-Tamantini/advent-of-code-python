from models.common.graphs import UndirectedGraph

from ..cliques import three_cliques


def test_all_cliques_of_size_three_are_found():
    graph = UndirectedGraph()
    graph.add_edge("kh", "tc")
    graph.add_edge("qp", "kh")
    graph.add_edge("de", "cg")
    graph.add_edge("ka", "co")
    graph.add_edge("yn", "aq")
    graph.add_edge("qp", "ub")
    graph.add_edge("cg", "tb")
    graph.add_edge("vc", "aq")
    graph.add_edge("tb", "ka")
    graph.add_edge("wh", "tc")
    graph.add_edge("yn", "cg")
    graph.add_edge("kh", "ub")
    graph.add_edge("ta", "co")
    graph.add_edge("de", "co")
    graph.add_edge("tc", "td")
    graph.add_edge("tb", "wq")
    graph.add_edge("wh", "td")
    graph.add_edge("ta", "ka")
    graph.add_edge("td", "qp")
    graph.add_edge("aq", "cg")
    graph.add_edge("wq", "ub")
    graph.add_edge("ub", "vc")
    graph.add_edge("de", "ta")
    graph.add_edge("wq", "aq")
    graph.add_edge("wq", "vc")
    graph.add_edge("wh", "yn")
    graph.add_edge("ka", "de")
    graph.add_edge("kh", "ta")
    graph.add_edge("co", "tc")
    graph.add_edge("wh", "qp")
    graph.add_edge("tb", "vc")
    graph.add_edge("td", "yn")
    cliques = set(three_cliques(graph))
    assert set(cliques) == {
        frozenset(["aq", "cg", "yn"]),
        frozenset(["aq", "vc", "wq"]),
        frozenset(["co", "de", "ka"]),
        frozenset(["co", "de", "ta"]),
        frozenset(["co", "ka", "ta"]),
        frozenset(["de", "ka", "ta"]),
        frozenset(["kh", "qp", "ub"]),
        frozenset(["qp", "td", "wh"]),
        frozenset(["tb", "vc", "wq"]),
        frozenset(["tc", "td", "wh"]),
        frozenset(["td", "wh", "yn"]),
        frozenset(["ub", "vc", "wq"]),
    }
