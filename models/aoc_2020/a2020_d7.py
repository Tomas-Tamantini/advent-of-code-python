from dataclasses import dataclass
from typing import Iterator
from models.graphs import DirectedGraph, explore_with_bfs


@dataclass(frozen=True)
class LuggageRule:
    bag: str
    contains: dict[str, int]


class LuggageRules:
    def __init__(self) -> None:
        self._graph = DirectedGraph()

    def add_rule(self, rule: LuggageRule) -> None:
        for color in rule.contains:
            self._graph.add_edge(source=color, target=rule.bag)

    def possible_colors_of_outermost_bag(self, color: str) -> Iterator[str]:
        for containing_color, _ in explore_with_bfs(
            graph=self._graph, initial_node=color
        ):
            if containing_color != color:
                yield containing_color
