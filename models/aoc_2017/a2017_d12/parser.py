from models.common.io import InputReader
from .program_graph import ProgramGraph


def parse_program_graph(input_reader: InputReader) -> ProgramGraph:
    graph = ProgramGraph()
    for line in input_reader.readlines():
        parts = line.strip().split(" ")
        node = int(parts[0])
        for neighbor in parts[2:]:
            graph.add_edge(node, int(neighbor.replace(",", "")))
    return graph
