from models.common.io import InputFromString
from ..parser import parse_seating_arrangement


def test_parse_seating_arrangement():
    graph_str = """Alice would gain 54 happiness units by sitting next to Bob.
                   Bob would lose 7 happiness units by sitting next to Carol.
                   Carol would lose 62 happiness units by sitting next to Alice."""
    graph = parse_seating_arrangement(InputFromString(graph_str))
    assert graph.round_trip_itinerary_min_cost() == -15
    assert graph.round_trip_itinerary_max_cost() == float("inf")
