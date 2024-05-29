from models.common.vectors import Vector2D
from models.common.graphs import explore_with_bfs, travelling_salesman
from typing import Iterator


class AirDuctMaze:
    def __init__(self, blueprint: list[str]) -> None:
        self._blueprint = blueprint
        self._positions_points_of_interest = {}
        self._labels_points_of_interest = {}
        for y, line in enumerate(blueprint):
            for x, char in enumerate(line):
                if char.isdigit():
                    self._positions_points_of_interest[char] = Vector2D(x, y)
                    self._labels_points_of_interest[Vector2D(x, y)] = char

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions():
            if self._blueprint[neighbor.y][neighbor.x] != "#":
                yield neighbor

    def _distances_to_larger_points_of_interest(
        self, point_of_interest: chr
    ) -> dict[chr, int]:
        num_pois_larger = len(
            [
                poi
                for poi in self._positions_points_of_interest
                if poi > point_of_interest
            ]
        )
        distances = {}
        while len(distances) < num_pois_larger:
            initial_node = self._positions_points_of_interest[point_of_interest]
            for node, distance in explore_with_bfs(self, initial_node):
                if node in self._labels_points_of_interest:
                    other_poi = self._labels_points_of_interest[node]
                    if other_poi > point_of_interest:
                        distances[other_poi] = distance
        return distances

    def pairwise_distances(self) -> dict[tuple[str, str], int]:
        distances = {}
        for poi_id in self._positions_points_of_interest.keys():
            distances_from_poi = self._distances_to_larger_points_of_interest(poi_id)
            for other_poi_id, distance in distances_from_poi.items():
                distances[(poi_id, other_poi_id)] = distance
        return distances

    def min_num_steps_to_visit_points_of_interest(
        self, must_return_to_origin: bool
    ) -> int:
        distances = self.pairwise_distances()
        return travelling_salesman("0", distances, must_return_to_origin)
