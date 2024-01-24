from typing import Protocol, Hashable, Iterator
from collections import defaultdict


class Graph(Protocol):
    def neighbors(self, node: Hashable) -> Iterator[Hashable]:
        ...


class DirectedGraph(Protocol):
    def nodes(self) -> Iterator[Hashable]:
        ...

    def incoming(self, node: Hashable) -> Iterator[Hashable]:
        ...

    def outgoing(self, node: Hashable) -> Iterator[Hashable]:
        ...


class MutableDirectedGraph:
    def __init__(self) -> None:
        self._incoming = defaultdict(set)
        self._outgoing = defaultdict(set)

    def add_node(self, node: Hashable) -> None:
        if node not in self._incoming:
            self._incoming[node] = set()

    def add_edge(self, source: Hashable, target: Hashable) -> None:
        self._incoming[target].add(source)
        self._outgoing[source].add(target)
        self.add_node(source)

    def nodes(self) -> Iterator[Hashable]:
        yield from self._incoming.keys()

    def incoming(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._incoming[node]

    def outgoing(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._outgoing[node]
