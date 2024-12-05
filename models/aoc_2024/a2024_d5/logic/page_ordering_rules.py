from itertools import combinations
from typing import Iterable
from models.common.graphs import DirectedGraph
from .page_ordering_rule import PageOrderingRule


class _DAG(DirectedGraph):
    def __init__(self) -> None:
        super().__init__()
        self._cached_reachable = dict()

    def reachable_from(self, node: int) -> set[int]:
        if node in self._cached_reachable:
            return self._cached_reachable[node]
        _reachable = set()
        for neighbor in self.neighbors(node):
            _reachable.add(neighbor)
            _reachable.update(self.reachable_from(neighbor))
        self._cached_reachable[node] = _reachable
        return _reachable


class PageOrderingRules:
    def __init__(self, rules: Iterable[PageOrderingRule]) -> None:
        self._violations_graph = _DAG()
        for rule in rules:
            self._violations_graph.add_edge(rule.page_after, rule.page_before)

    def is_in_correct_order(self, update: tuple[int, ...]) -> bool:
        return all(
            page_after not in self._violations_graph.reachable_from(page_before)
            for page_before, page_after in combinations(update, 2)
        )
