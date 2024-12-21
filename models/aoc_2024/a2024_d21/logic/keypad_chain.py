from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection

from .keypad_layout import KeypadLayout
from .keypad_robot import KeypadRobot


@dataclass(frozen=True)
class _MemoizedId:
    button_pair: tuple[chr, chr]
    num_robots: int


def _direction_to_btn(direction: CardinalDirection) -> chr:
    return {
        CardinalDirection.NORTH: "^",
        CardinalDirection.SOUTH: "v",
        CardinalDirection.WEST: "<",
        CardinalDirection.EAST: ">",
    }[direction]


class KeypadChain:
    def __init__(
        self,
        numeric_robot: KeypadRobot,
        directional_robot: KeypadRobot,
        num_directional_robots: int,
    ) -> None:
        self._numeric_robot = numeric_robot
        self._directional_robot = directional_robot
        self._num_directional_robots = num_directional_robots
        self._memoized_results = dict()

    def _numeric_button_pairs(self, code: str) -> Iterator[tuple[chr, chr]]:
        current_btn = self._numeric_robot.initial_button
        for next_btn in code:
            yield current_btn, next_btn
            current_btn = next_btn

    def min_num_keypad_presses(self, code: str) -> int:
        return sum(
            self._min_presses_between_btn_pair(
                btn_pair,
                self._numeric_robot.keypad_layout,
                self._num_directional_robots,
            )
            for btn_pair in self._numeric_button_pairs(code)
        )

    def _min_presses_between_btn_pair(
        self,
        button_pair: tuple[chr, chr],
        keypad_layout: KeypadLayout,
        num_directional_robots: int,
    ) -> int:
        return min(
            self._min_presses_for_path(path, num_directional_robots)
            for path in keypad_layout.shortest_paths_between_buttons(*button_pair)
        )

    def _directional_button_pairs(
        self, path: tuple[CardinalDirection, ...]
    ) -> Iterator[tuple[chr, chr]]:
        current_btn = self._directional_robot.initial_button
        for next_btn in path:
            yield current_btn, _direction_to_btn(next_btn)
            current_btn = _direction_to_btn(next_btn)
        yield current_btn, self._directional_robot.initial_button

    def _min_presses_for_path(
        self, path: tuple[CardinalDirection, ...], num_directional_robots: int
    ) -> int:
        return sum(
            self._min_presses_between_directional_pair(
                btn_pair,
                num_directional_robots - 1,
            )
            for btn_pair in self._directional_button_pairs(path)
        )

    def _min_presses_between_directional_pair(
        self, button_pair: tuple[chr, chr], num_directional_robots: int
    ) -> int:
        if num_directional_robots < 0:
            return 1
        memoized_id = _MemoizedId(button_pair, num_directional_robots)
        if memoized_id not in self._memoized_results:
            result = self._min_presses_between_btn_pair(
                button_pair,
                self._directional_robot.keypad_layout,
                num_directional_robots,
            )
            self._memoized_results[memoized_id] = result
        return self._memoized_results[memoized_id]
