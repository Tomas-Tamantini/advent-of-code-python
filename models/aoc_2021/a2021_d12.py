from dataclasses import dataclass
from typing import Iterator, Optional
from collections import defaultdict


@dataclass(frozen=True)
class UnderwaterCave:
    name: str
    is_small: bool


class UnderwaterCaveExplorer:
    def __init__(
        self,
        connections: dict[UnderwaterCave, set[UnderwaterCave]],
        start_cave_name: str,
        end_cave_name: str,
    ) -> None:
        self._connections = self._complete_connections(connections)
        self._start_cave = self._get_cave_by_name(start_cave_name)
        self._end_cave = self._get_cave_by_name(end_cave_name)

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
        self, current_path: list[UnderwaterCave]
    ) -> Iterator[list[UnderwaterCave]]:
        if current_path[-1] == self._end_cave:
            yield current_path
        else:
            for neighbor in self._connections[current_path[-1]]:
                if not neighbor.is_small or neighbor not in current_path:
                    yield from self._explore_paths(
                        current_path=current_path + [neighbor]
                    )

    def all_paths(self) -> Iterator[list[UnderwaterCave]]:
        if self._start_cave is None or self._end_cave is None:
            return
        current_path = [self._start_cave]
        yield from self._explore_paths(current_path=current_path)
