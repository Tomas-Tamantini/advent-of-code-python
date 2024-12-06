from math import inf
from typing import Hashable, Iterator, Protocol


class _StateExplorer(Protocol):
    def objective_value(self, state: Hashable) -> float: ...

    def upper_bound_on_objective_value(self, state: Hashable) -> float: ...

    def children_states(self, state: Hashable) -> Iterator[Hashable]: ...


def maximize_with_branch_and_bound(
    initial_state: Hashable, state_explorer: _StateExplorer, lower_bound: float = -inf
) -> int:
    explored_states = set()
    explore_stack = [initial_state]
    max_value = lower_bound - 1e-9
    while explore_stack:
        current_state = explore_stack.pop()
        if current_state in explored_states:
            continue
        if state_explorer.upper_bound_on_objective_value(current_state) > max_value:
            max_value = max(max_value, state_explorer.objective_value(current_state))
            for next_state in state_explorer.children_states(current_state):
                explore_stack.append(next_state)
        explored_states.add(current_state)
    return max_value
