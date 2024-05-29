from models.common.io import InputReader
from .seating_arrangements import SeatingArrangements


def parse_seating_arrangement(input_reader: InputReader) -> SeatingArrangements:
    graph = SeatingArrangements()
    for line in input_reader.readlines():
        sentence_parts = line.strip().split(" ")
        node_a = sentence_parts[0].strip()
        node_b = sentence_parts[-1].replace(".", "").strip()
        cost = int(sentence_parts[3])
        if "lose" in line:
            cost = -cost
        graph.add_edge(node_a, node_b, cost)
    return graph
