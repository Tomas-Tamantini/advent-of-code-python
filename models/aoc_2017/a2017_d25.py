from dataclasses import dataclass
from collections import defaultdict
from typing import Optional
from models.common.io import ProgressBar


@dataclass(frozen=True)
class TuringState:
    state_id: str
    current_value: int


@dataclass(frozen=True)
class TuringRule:
    next_state_id: str
    write_value: int
    move: int


class TuringMachine:
    def __init__(self) -> None:
        self._tape = defaultdict(int)

    @property
    def sum_tape_values(self) -> int:
        return sum(self._tape.values())

    def run(
        self,
        transition_rules: dict[TuringState, TuringRule],
        initial_state: str,
        steps: int,
        progress_bar: Optional[ProgressBar] = None,
    ) -> None:
        self._tape = defaultdict(int)
        state = initial_state
        cursor = 0
        for step in range(steps):
            if progress_bar is not None:
                progress_bar.update(step, steps)
            current_value = self._tape[cursor]
            rule = transition_rules[TuringState(state, current_value)]
            self._tape[cursor] = rule.write_value
            cursor += rule.move
            state = rule.next_state_id
