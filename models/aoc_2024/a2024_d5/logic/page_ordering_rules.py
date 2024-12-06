from itertools import combinations
from typing import Iterable, Iterator

from models.common.graphs import DirectedGraph, topological_sorting

from .page_ordering_rule import PageOrderingRule


class _DAG(DirectedGraph):
    def __init__(self) -> None:
        super().__init__()
        self._cached_reachable = dict()

    def reachable_from(self, node: int) -> set[int]:
        if node in self._cached_reachable:
            return self._cached_reachable[node]
        reachable = set()
        for neighbor in self.neighbors(node):
            reachable.add(neighbor)
            reachable.update(self.reachable_from(neighbor))
        self._cached_reachable[node] = reachable
        return reachable


class PageOrderingRules:
    def __init__(self, rules: Iterable[PageOrderingRule]) -> None:
        self._rules = rules

    def _pertinent_rules(self, update: tuple[int, ...]) -> Iterator[PageOrderingRule]:
        for rule in self._rules:
            if rule.page_before in update and rule.page_after in update:
                yield rule

    def is_in_correct_order(self, update: tuple[int, ...]) -> bool:
        violations_graph = _DAG()
        for rule in self._pertinent_rules(update):
            violations_graph.add_edge(rule.page_after, rule.page_before)
        return all(
            page_after not in violations_graph.reachable_from(page_before)
            for page_before, page_after in combinations(update, 2)
        )

    def sort_update(self, update: tuple[int, ...]) -> tuple[int, ...]:
        sorting_dag = DirectedGraph()
        for rule in self._pertinent_rules(update):
            sorting_dag.add_edge(rule.page_before, rule.page_after)
        return tuple(topological_sorting(sorting_dag))
