from typing import Protocol, Hashable, Iterator
from collections import defaultdict
from math import inf


class GraphProtocol(Protocol):
    def neighbors(self, node: Hashable) -> Iterator[Hashable]: ...


class DirectedGraphProtocol(Protocol):
    def nodes(self) -> Iterator[Hashable]: ...

    def incoming(self, node: Hashable) -> Iterator[Hashable]: ...

    def outgoing(self, node: Hashable) -> Iterator[Hashable]: ...


class UndirectedGraph:
    def __init__(self) -> None:
        self._adjacencies = defaultdict(set)

    def add_node(self, node: Hashable) -> None:
        if node not in self._adjacencies:
            self._adjacencies[node] = set()

    def add_edge(self, node_a: Hashable, node_b: Hashable) -> None:
        self._adjacencies[node_a].add(node_b)
        self._adjacencies[node_b].add(node_a)

    def nodes(self) -> Iterator[Hashable]:
        yield from self._adjacencies.keys()

    def neighbors(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._adjacencies[node]


class WeightedUndirectedGraph:

    def __init__(self) -> None:
        self._adjacencies = defaultdict(dict)

    def add_node(self, node: Hashable) -> None:
        if node not in self._adjacencies:
            self._adjacencies[node] = dict()

    def add_edge(self, node_a: Hashable, node_b: Hashable, weight: float) -> None:
        self._adjacencies[node_a][node_b] = weight
        self._adjacencies[node_b][node_a] = weight

    def nodes(self) -> Iterator[Hashable]:
        yield from self._adjacencies.keys()

    def neighbors(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._adjacencies[node].keys()

    def weight(self, node_a: Hashable, node_b: Hashable) -> float:
        return self._adjacencies[node_a].get(node_b, inf)


class DirectedGraph:
    def __init__(self) -> None:
        self._incoming = defaultdict(set)
        self._outgoing = defaultdict(set)

    def add_node(self, node: Hashable) -> None:
        if node not in self._incoming:
            self._incoming[node] = set()

    def remove_node(self, node: Hashable) -> None:
        for neighbor in self._incoming[node]:
            self._outgoing[neighbor].remove(node)
        for neighbor in self._outgoing[node]:
            self._incoming[neighbor].remove(node)
        del self._incoming[node]
        del self._outgoing[node]

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


class WeightedDirectedGraph:
    def __init__(self) -> None:
        self._incoming = defaultdict(dict)
        self._outgoing = defaultdict(dict)

    def add_node(self, node: Hashable) -> None:
        if node not in self._incoming:
            self._incoming[node] = dict()

    def add_edge(self, source: Hashable, target: Hashable, weight: float) -> None:
        self._incoming[target][source] = weight
        self._outgoing[source][target] = weight
        self.add_node(source)

    def nodes(self) -> Iterator[Hashable]:
        yield from self._incoming.keys()

    def incoming(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._incoming[node]

    def outgoing(self, node: Hashable) -> Iterator[Hashable]:
        yield from self._outgoing[node]

    def weight(self, source: Hashable, target: Hashable) -> float:
        return self._incoming[target].get(source, inf)
