from models.aoc_2015 import SeatingArrangements


def test_graph_with_two_nodes_has_single_possible_itinerary_cost():
    graph = SeatingArrangements()
    graph.add_edge("a", "b", 100)
    graph.add_edge("b", "a", 200)
    assert graph.round_trip_itinerary_min_cost() == 300
    assert graph.round_trip_itinerary_max_cost() == 300


def test_graph_finds_shortest_and_longest_possible_itinerary():
    graph = SeatingArrangements()
    graph.add_edge("a", "b", 100)
    graph.add_edge("b", "c", 100)
    graph.add_edge("c", "a", 100)

    graph.add_edge("a", "c", 200)
    graph.add_edge("c", "b", 200)
    graph.add_edge("b", "a", 200)
    assert graph.round_trip_itinerary_min_cost() == 300
    assert graph.round_trip_itinerary_max_cost() == 600


def test_can_optimize_paths_going_both_ways():
    graph = SeatingArrangements()

    graph.add_edge("a", "b", 54)
    graph.add_edge("a", "c", -79)
    graph.add_edge("a", "d", -2)

    graph.add_edge("b", "a", 83)
    graph.add_edge("b", "c", -7)
    graph.add_edge("b", "d", -63)

    graph.add_edge("c", "a", -62)
    graph.add_edge("c", "b", 60)
    graph.add_edge("c", "d", 55)

    graph.add_edge("d", "a", 46)
    graph.add_edge("d", "b", -7)
    graph.add_edge("d", "c", 41)

    assert graph.both_ways_trip_max_cost() == 330
