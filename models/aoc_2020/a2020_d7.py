from dataclasses import dataclass
from typing import Iterator
from models.graphs import WeightedDirectedGraph, explore_with_bfs


@dataclass(frozen=True)
class LuggageRule:
    bag: str
    contains: dict[str, int]


class LuggageRules:
    def __init__(self) -> None:
        self._graph = WeightedDirectedGraph()

    def add_rule(self, rule: LuggageRule) -> None:
        for color, amount in rule.contains.items():
            self._graph.add_edge(source=color, target=rule.bag, weight=amount)

    def possible_colors_of_outermost_bag(self, color: str) -> Iterator[str]:
        for containing_color, _ in explore_with_bfs(
            graph=self._graph, initial_node=color
        ):
            if containing_color != color:
                yield containing_color

    def number_of_bags_contained_inside(
        self, color: str, memoized_values: dict[str, int] = None
    ) -> int:
        if memoized_values is None:
            memoized_values = dict()
        if color in memoized_values:
            return memoized_values[color]
        total = 0
        for child in self._graph.incoming(color):
            amount = self._graph.weight(child, color)
            total += amount * (
                1 + self.number_of_bags_contained_inside(child, memoized_values)
            )
        memoized_values[color] = total
        return total
