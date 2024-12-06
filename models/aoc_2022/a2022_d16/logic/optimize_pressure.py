from typing import Iterator

from models.common.optimization.branch_and_bound import maximize_with_branch_and_bound

from .volcano import Volcano
from .volcano_state import VolcanoState
from .volcano_worker import VolcanoWorker


class _VolcanoExplorer:
    def __init__(self, volcano: Volcano) -> None:
        self._volcano = volcano

    @staticmethod
    def objective_value(state: VolcanoState) -> float:
        return state.pressure_released

    def upper_bound_on_objective_value(self, state: VolcanoState) -> float:
        return state.pressure_release_upper_bound(self._volcano)

    def children_states(self, state: VolcanoState) -> Iterator[VolcanoState]:
        yield from state.next_states(self._volcano)


def maximum_pressure_release(
    volcano: Volcano, num_workers: int, lower_bound: int = 0
) -> int:
    inital_state = VolcanoState(
        elapsed_time=0,
        pressure_released=0,
        open_valves=set(),
        workers=tuple(
            VolcanoWorker(is_idle=True, valve=volcano.starting_valve)
            for _ in range(num_workers)
        ),
    )
    explorer = _VolcanoExplorer(volcano)
    return maximize_with_branch_and_bound(inital_state, explorer, lower_bound)
