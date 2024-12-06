from models.common.graphs import UndirectedGraph
from models.common.io import InputReader


def _parse_edges(line: str, graph: UndirectedGraph) -> None:
    node, neighbors = line.split(":")
    for neighbor in neighbors.split():
        graph.add_edge(node.strip(), neighbor.strip())


def parse_wiring_diagram(input_reader: InputReader) -> UndirectedGraph:
    graph = UndirectedGraph()
    for line in input_reader.read_stripped_lines():
        _parse_edges(line, graph)
    return graph
