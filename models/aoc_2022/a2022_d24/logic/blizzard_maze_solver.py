from typing import Iterator
from models.common.graphs import min_path_length_with_bfs
from .blizzard_valley import BlizzardValley
from .blizzard_navigator import BlizzardNavigator


class BlizzardMazeSolver:
    def __init__(self, valley: BlizzardValley):
        self._valley = valley

    def first_state(self) -> BlizzardNavigator:
        return BlizzardNavigator(position=self._valley._entrance, time=0)

    def is_terminal(self, state: BlizzardNavigator) -> bool:
        return state.position == self._valley._exit

    def neighbors(self, node: BlizzardNavigator) -> Iterator[BlizzardNavigator]:
        for neighbor in node.next_states():
            if self._valley.position_is_free_at_time(neighbor.position, neighbor.time):
                yield neighbor

    def min_steps_to_exit(self) -> int:
        return min_path_length_with_bfs(
            self, initial_node=self.first_state(), is_final_state=self.is_terminal
        )
