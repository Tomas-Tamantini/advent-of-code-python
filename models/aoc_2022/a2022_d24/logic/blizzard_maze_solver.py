from typing import Iterator
from models.common.graphs import min_path_length_with_bfs
from .blizzard_valley import BlizzardValley
from .blizzard_navigator import BlizzardNavigator


class BlizzardMazeSolver:
    def __init__(self, valley: BlizzardValley):
        self._valley = valley
        self._goal = valley.exit

    def first_state(self) -> BlizzardNavigator:
        return BlizzardNavigator(position=self._valley.entrance, time=0)

    def is_terminal(self, state: BlizzardNavigator) -> bool:
        return state.position == self._goal

    def _distance_from_goal(self, state: BlizzardNavigator) -> int:
        return state.position.manhattan_distance(self._goal)

    def neighbors(self, node: BlizzardNavigator) -> Iterator[BlizzardNavigator]:
        candidates = (
            neighbor
            for neighbor in node.next_states()
            if self._valley.position_is_free_at_time(neighbor.position, neighbor.time)
        )
        yield from sorted(candidates, key=lambda c: self._distance_from_goal(c))

    def _steps_from_entrance_to_exit(self, initial_timestamp: int) -> int:
        self._goal = self._valley.exit
        state = BlizzardNavigator(
            position=self._valley.entrance, time=initial_timestamp
        )
        return min_path_length_with_bfs(
            self, initial_node=state, is_final_state=self.is_terminal
        )

    def _steps_from_exit_to_entrance(self, initial_timestamp: int) -> int:
        self._goal = self._valley.entrance
        state = BlizzardNavigator(position=self._valley.exit, time=initial_timestamp)
        return min_path_length_with_bfs(
            self, initial_node=state, is_final_state=self.is_terminal
        )

    def min_steps_to_exit(self, num_returns_to_start: int = 0) -> int:
        steps = self._steps_from_entrance_to_exit(initial_timestamp=0)
        for _ in range(num_returns_to_start):
            steps += self._steps_from_exit_to_entrance(initial_timestamp=steps)
            steps += self._steps_from_entrance_to_exit(initial_timestamp=steps)

        return steps
