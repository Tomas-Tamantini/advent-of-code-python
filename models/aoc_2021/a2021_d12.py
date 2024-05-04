from dataclasses import dataclass
from typing import Iterator, Optional
from collections import defaultdict


@dataclass(frozen=True)
class UnderwaterCave:
    name: str
    is_small: bool


class UnderwaterCaveExplorer:
    def __init__(self, connections: dict[UnderwaterCave, set[UnderwaterCave]]) -> None:
        self._connections = self._complete_connections(connections)

    @staticmethod
    def _complete_connections(
        connections: dict[UnderwaterCave, set[UnderwaterCave]]
    ) -> dict[UnderwaterCave, set[UnderwaterCave]]:
        complete_connections = defaultdict(set)
        for cave, neighbors in connections.items():
            complete_connections[cave].update(neighbors)
            for neighbor in neighbors:
                complete_connections[neighbor].add(cave)
        return complete_connections

    def _get_cave_by_name(self, name: str) -> Optional[UnderwaterCave]:
        try:
            return next(cave for cave in self._connections if cave.name == name)
        except StopIteration:
            return None

    def _explore_paths(
        self,
        current_path: list[UnderwaterCave],
        visited: set[UnderwaterCave],
        end_cave: UnderwaterCave,
    ) -> Iterator[list[UnderwaterCave]]:
        if current_path[-1] == end_cave:
            yield current_path
        else:
            for neighbor in self._connections[current_path[-1]]:
                if neighbor not in visited:
                    if neighbor.is_small:
                        new_visited = visited.copy()
                        new_visited.add(neighbor)
                    else:
                        new_visited = visited
                    yield from self._explore_paths(
                        current_path=current_path + [neighbor],
                        visited=new_visited,
                        end_cave=end_cave,
                    )

    def all_paths(
        self, start_cave_name: str, end_cave_name: str
    ) -> Iterator[list[UnderwaterCave]]:
        start_cave = self._get_cave_by_name(start_cave_name)
        end_cave = self._get_cave_by_name(end_cave_name)
        if start_cave is None or end_cave is None:
            return
        current_path = [start_cave]
        visited = {start_cave}
        yield from self._explore_paths(
            current_path=current_path, visited=visited, end_cave=end_cave
        )
