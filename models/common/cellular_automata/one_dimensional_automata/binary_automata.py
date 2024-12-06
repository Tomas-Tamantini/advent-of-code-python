from typing import Iterator, Optional

from models.common.cellular_automata.two_state_automata import (
    TwoStateCellVicinity,
    two_state_automaton_next_state,
)


class OneDimensionalBinaryCelullarAutomaton:
    def __init__(
        self,
        rules: dict[tuple[int, ...], int],
        min_idx: Optional[int] = None,
        max_idx: Optional[int] = None,
    ) -> None:
        self._min_idx = min_idx
        self._max_idx = max_idx
        self._rules = rules
        self._radius_of_influence = self._get_radius_of_influence(rules)

    @staticmethod
    def _get_radius_of_influence(rules: dict[tuple[int, ...], int]) -> int:
        if not rules:
            return 0
        rule_length = -1
        for rule, rule_value in rules.items():
            if len(rule) % 2 == 0:
                raise ValueError("Rules must have odd length")
            if all(r == 0 for r in rule) and rule_value == 1:
                raise ValueError("Rule for all zeros must be zero")
            if rule_length == -1:
                rule_length = len(rule)
            elif rule_length != len(rule):
                raise ValueError("All rules must have the same length")
        return (rule_length - 1) // 2

    def is_within_bounds(self, cell: int) -> bool:
        if self._min_idx is not None and cell < self._min_idx:
            return False
        if self._max_idx is not None and cell > self._max_idx:
            return False
        return True

    def neighbors(self, cell: int) -> Iterator[int]:
        min_idx = cell - self._radius_of_influence
        max_idx = cell + self._radius_of_influence
        for i in range(min_idx, max_idx + 1):
            if i != cell:
                yield i

    def cell_is_alive_in_next_generation(self, vicinity: TwoStateCellVicinity) -> bool:
        configuration = []
        min_idx = vicinity.center_cell - self._radius_of_influence
        max_idx = vicinity.center_cell + self._radius_of_influence
        for i in range(min_idx, max_idx + 1):
            if i == vicinity.center_cell:
                configuration.append(1 if vicinity.center_cell_is_alive else 0)
            else:
                configuration.append(1 if i in vicinity.alive_neighbors else 0)
        return bool(self._rules.get(tuple(configuration), 0))

    def _neighboring_state(self, current_state: set[int], idx: int) -> list[int]:
        return [
            int(j in current_state)
            for j in range(
                idx - self._radius_of_influence,
                idx + self._radius_of_influence + 1,
            )
        ]

    def next_state(self, current_state: set[int]) -> set[int]:
        return two_state_automaton_next_state(self, current_state)
