from models.aoc_2015 import CityRouter


def test_graph_with_two_nodes_has_single_possible_itinerary_distance():
    graph = CityRouter()
    graph.add_edge("a", "b", 100)
    assert graph.shortest_complete_itinerary_distance() == 100


def test_graph_finds_shortest_possible_itinerary():
    graph = CityRouter()
    graph.add_edge("a", "b", 100)
    graph.add_edge("a", "c", 100)
    graph.add_edge("b", "c", 150)
    assert graph.shortest_complete_itinerary_distance() == 200


def test_graph_finds_longest_possible_itinerary():
    graph = CityRouter()
    graph.add_edge("a", "b", 100)
    graph.add_edge("a", "c", 100)
    graph.add_edge("b", "c", 150)
    assert graph.longest_complete_itinerary_distance() == 250
