# TODO: Refactor tests and implementation

from typing import Iterator
from .amphipod_burrow import AmphipodBurrow, BurrowPosition
from .amphipod import Amphipod, AmphipodArrangement

from math import inf
from dataclasses import dataclass, field
from queue import PriorityQueue


@dataclass(frozen=True, order=True)
class _PriorityItem:
    priority: float
    item: AmphipodArrangement = field(compare=False)


class AmphipodSorter:
    def __init__(self, burrow: AmphipodBurrow):
        self._burrow = burrow

    def weight(self, node_a: AmphipodArrangement, node_b: AmphipodArrangement) -> int:
        return node_a.energy_to_move(node_b)

    def _possible_new_positions(
        self, amphipod: Amphipod, other_amphipods: set[Amphipod]
    ) -> Iterator[BurrowPosition]:
        if amphipod.num_moves == 0:
            occupied_positions = {amp.position for amp in other_amphipods}
            yield from self._burrow.reachable_hallway_positions(
                amphipod.position, occupied_positions
            )
        elif amphipod.num_moves == 1:
            room_position = self._burrow.reachable_room_position(
                amphipod, other_amphipods
            )
            if room_position is not None:
                yield room_position

    def is_terminal(self, node: AmphipodArrangement) -> bool:
        return all(self._burrow.is_in_proper_room(amp) for amp in node.amphipods)

    def neighbors(self, node: AmphipodArrangement) -> Iterator[AmphipodArrangement]:
        for i, amphipod in enumerate(node.amphipods):
            other_amphipods = {amp for amp in node.amphipods if amp != amphipod}
            for new_position in self._possible_new_positions(amphipod, other_amphipods):
                new_amphipods = list(node.amphipods)
                new_amphipods[i] = amphipod.move(new_position)
                yield AmphipodArrangement(tuple(new_amphipods))

    def min_energy_to_organize(self, initial_arrangement: AmphipodArrangement) -> int:
        _, energy = modified_dijkstra(initial_arrangement, self)
        return energy


def modified_dijkstra(
    origin: AmphipodArrangement, graph: AmphipodSorter
) -> tuple[list[AmphipodArrangement], float]:
    distances = {origin: 0}
    previous = {origin: None}
    queue = PriorityQueue()
    queue.put(_PriorityItem(0, origin))

    while not queue.empty():
        current = queue.get()
        current_node = current.item
        current_distance = current.priority

        if graph.is_terminal(current_node):
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous[current_node]
            return path[::-1], current_distance

        for neighbor in graph.neighbors(current_node):
            distance = current_distance + graph.weight(current_node, neighbor)
            if distance < distances.get(neighbor, inf):
                distances[neighbor] = distance
                previous[neighbor] = current_node
                queue.put(_PriorityItem(distance, neighbor))

    raise ValueError("No path found")
