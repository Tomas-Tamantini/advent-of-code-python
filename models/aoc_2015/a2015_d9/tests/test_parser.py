from models.common.io import InputFromString

from ..parser import parse_undirected_graph


def test_parse_undirected_graph() -> None:
    graph_str = """a to b = 100
                   a to c = 100
                   b to c = 150"""
    graph = parse_undirected_graph(InputFromString(graph_str))
    assert graph.shortest_complete_itinerary_distance() == 200
