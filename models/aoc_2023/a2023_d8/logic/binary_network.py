from typing import Iterable
from dataclasses import dataclass
from models.common.number_theory import lcm
from .network_step import NetworkStep


@dataclass(frozen=True)
class _PeriodicWalk:
    aperiodic_indices_in_end_nodes: Iterable[int]
    periodic_indices_in_end_nodes: Iterable[int]
    period: int

    def is_simple_periodic(self) -> bool:
        return (
            (len(self.aperiodic_indices_in_end_nodes) == 0)
            and (len(self.periodic_indices_in_end_nodes) == 1)
            and (self.periodic_indices_in_end_nodes[0] == self.period)
        )


@dataclass(frozen=True)
class _TravelerState:
    current_node: str
    current_step_idx: int


class BinaryNetwork:
    def __init__(
        self, connections: dict[str, tuple[str, str]], steps: list[NetworkStep]
    ) -> None:
        self._connections = connections
        self._steps = steps

    def _next_state(self, current_state: _TravelerState) -> _TravelerState:
        current_step = self._steps[current_state.current_step_idx]
        next_node = self._connections[current_state.current_node][current_step]
        next_step_idx = (current_state.current_step_idx + 1) % len(self._steps)
        return _TravelerState(next_node, next_step_idx)

    def _periodic_walk(self, start_node: str, end_nodes: set[str]) -> _PeriodicWalk:
        state = _TravelerState(start_node, current_step_idx=0)
        seen_states = [state]
        seen_states_indices = {state: 0}
        period_start = -1
        while True:
            state = self._next_state(state)
            if state in seen_states_indices:
                period_start = seen_states_indices[state]
                break
            else:
                seen_states_indices[state] = len(seen_states)
                seen_states.append(state)
        period = len(seen_states) - period_start
        aperiodic_terms = [
            i
            for i, state in enumerate(seen_states[:period_start])
            if state.current_node in end_nodes
        ]
        periodic_terms = [
            i + period_start
            for i, state in enumerate(seen_states[period_start:])
            if state.current_node in end_nodes
        ]
        return _PeriodicWalk(aperiodic_terms, periodic_terms, period)

    def num_steps_to_finish(
        self, start_nodes: Iterable[str], end_nodes: Iterable[str]
    ) -> int:
        set_end_nodes = set(end_nodes)
        walks = [
            self._periodic_walk(start_node, set_end_nodes) for start_node in start_nodes
        ]
        # TODO: This line below only works for simple periodics. Implement other cases
        return lcm(*list(walk.period for walk in walks))
