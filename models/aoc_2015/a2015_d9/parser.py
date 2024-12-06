from models.common.io import InputReader

from .city_router import CityRouter


def parse_undirected_graph(input_reader: InputReader) -> CityRouter:
    graph = CityRouter()
    for line in input_reader.readlines():
        nodes_str, distance_str = line.split("=")
        nodes = [n.strip() for n in nodes_str.split("to")]
        distance = int(distance_str)
        graph.add_edge(*nodes, distance)
    return graph
