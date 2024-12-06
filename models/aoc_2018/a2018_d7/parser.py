from models.common.graphs import DirectedGraph
from models.common.io import InputReader


def parse_directed_graph(input_reader: InputReader) -> DirectedGraph:
    graph = DirectedGraph()
    for line in input_reader.readlines():
        parts = line.strip().split(" ")
        graph.add_edge(parts[1], parts[-3])
    return graph
