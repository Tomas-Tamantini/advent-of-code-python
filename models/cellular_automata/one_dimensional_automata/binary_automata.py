from typing import Optional


class OneDimensionalBinaryCelullarAutomaton:
    def __init__(self, rules: dict[tuple[int, ...], int]) -> None:
        self._rules = rules
        self._radius_of_influence = self._get_radius_of_influence(rules)

    @staticmethod
    def _get_radius_of_influence(rules: dict[tuple[int, ...], int]) -> int:
        if not rules:
            return 0
        rule_length = -1
        for rule in rules:
            if len(rule) % 2 == 0:
                raise ValueError("Rules must have odd length")
            if all(r == 0 for r in rule) and rules[rule] == 1:
                raise ValueError("Rule for all zeros must be zero")
            if rule_length == -1:
                rule_length = len(rule)
            elif rule_length != len(rule):
                raise ValueError("All rules must have the same length")
        return (rule_length - 1) // 2

    def _neighboring_state(self, current_state: set[int], idx: int) -> list[int]:
        return [
            int(j in current_state)
            for j in range(
                idx - self._radius_of_influence,
                idx + self._radius_of_influence + 1,
            )
        ]

    def _walk_neighboring_state_to_the_right(
        self, current_state: set[int], neighboring_state: list[int], idx: int
    ) -> None:
        neighboring_state.pop(0)
        idx_to_append = idx + 1 + self._radius_of_influence
        term_to_append = 1 if idx_to_append in current_state else 0
        neighboring_state.append(term_to_append)

    def next_state(
        self,
        current_state: set[int],
        min_idx: Optional[int] = None,
        max_idx: Optional[int] = None,
    ) -> set[int]:
        if not current_state:
            return set()
        next_state = set()
        if min_idx is None:
            min_idx = min(current_state) - self._radius_of_influence
        if max_idx is None:
            max_idx = max(current_state) + self._radius_of_influence
        neighboring_state = self._neighboring_state(current_state, min_idx)
        for i in range(min_idx, max_idx + 1):
            if self._rules.get(tuple(neighboring_state), 0):
                next_state.add(i)
            self._walk_neighboring_state_to_the_right(
                current_state, neighboring_state, i
            )
        return next_state
