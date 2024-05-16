from dataclasses import dataclass, field
from queue import PriorityQueue
from .amphipod_burrow import AmphipodBurrow
from typing import Iterator


class AmphipodSorter:
    def weighted_neighbors(
        self, burrow: AmphipodBurrow
    ) -> Iterator[tuple[AmphipodBurrow, int]]:
        yield from burrow.weighted_neighbors()

    def min_energy_to_sort(self, burrow: AmphipodBurrow) -> int:
        origin = burrow
        destination = burrow.terminal_state()
        _, energy = modified_dijkstra(origin, destination, self)
        return energy


# TODO: Modify original dijkstra and delete everything below


@dataclass(frozen=True, order=True)
class _PriorityItem:
    priority: float
    item: AmphipodBurrow = field(compare=False)


def modified_dijkstra(
    origin: AmphipodBurrow,
    destination: AmphipodBurrow,
    graph: AmphipodSorter,
) -> tuple[list[AmphipodBurrow], float]:
    distances = {origin: 0}
    previous = {origin: None}
    queue = PriorityQueue()
    queue.put(_PriorityItem(0, origin))

    while not queue.empty():
        current = queue.get()
        current_node = current.item
        current_distance = current.priority

        if current_node == destination:
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous[current_node]
            return path[::-1], current_distance

        for neighbor, weight in graph.weighted_neighbors(current_node):
            distance = current_distance + weight
            if distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = distance
                previous[neighbor] = current_node
                queue.put(_PriorityItem(distance, neighbor))

    raise ValueError("No path found")
