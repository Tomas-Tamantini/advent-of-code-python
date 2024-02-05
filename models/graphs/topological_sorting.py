from typing import Iterator, Hashable, Optional, Callable
from .graph import DirectedGraphProtocol


class _PriorityQueue:
    def __init__(
        self,
        compare_method: Optional[Callable[[Hashable, Hashable], bool]],
    ):
        self._queue = []
        self._compare_method = compare_method

    @property
    def empty(self) -> bool:
        return not self._queue

    def _insert_position(self, node: Hashable) -> int:
        if not self._compare_method:
            return len(self._queue)

        low = 0
        high = len(self._queue)
        while low < high:
            mid = (low + high) // 2
            if self._compare_method(node, self._queue[mid]):
                low = mid + 1
            else:
                high = mid
        return low

    def push(self, node: Hashable) -> None:
        self._queue.insert(self._insert_position(node), node)

    def pop(self) -> Hashable:
        return self._queue.pop()


def topological_sorting(
    dag: DirectedGraphProtocol,
    tie_breaker: Optional[Callable[[Hashable, Hashable], bool]] = None,
) -> Iterator[Hashable]:
    all_nodes = set(dag.nodes())
    nodes_to_visit = _PriorityQueue(tie_breaker)
    for node in all_nodes:
        if not set(dag.incoming(node)):
            nodes_to_visit.push(node)
    if nodes_to_visit.empty and all_nodes:
        raise ValueError("Cycle detected")
    visited = set()
    while not nodes_to_visit.empty:
        node = nodes_to_visit.pop()
        yield node
        visited.add(node)
        for child in dag.outgoing(node):
            if set(dag.incoming(child)).issubset(visited):
                nodes_to_visit.push(child)

    if len(visited) != len(set(all_nodes)):
        raise ValueError("Cycle detected")
