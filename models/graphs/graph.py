from typing import Protocol, Hashable, Iterator


class Graph(Protocol):
    def neighbors(self, node: Hashable) -> Iterator[Hashable]:
        ...
