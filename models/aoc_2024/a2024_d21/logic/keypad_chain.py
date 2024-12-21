from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection

from .keypad_layout import KeypadLayout
from .keypad_robot import KeypadRobot, KeypadRobots


def min_num_keypad_presses(
    code: str,
    numeric_robot: KeypadRobot,
    directional_robots: KeypadRobots,
) -> int:
    total_length = 0
    memoized_results = dict()
    for btn_pair in _numeric_button_pairs(code, numeric_robot.initial_button):
        total_length += _min_presses_between_button_pair(
            btn_pair, numeric_robot.keypad_layout, directional_robots, memoized_results
        )
    return total_length


def _numeric_button_pairs(code: str, initial_button: chr) -> Iterator[tuple[chr, chr]]:
    current_btn = initial_button
    for next_btn in code:
        yield current_btn, next_btn
        current_btn = next_btn


def _direction_to_btn(direction: CardinalDirection) -> chr:
    return {
        CardinalDirection.NORTH: "^",
        CardinalDirection.SOUTH: "v",
        CardinalDirection.WEST: "<",
        CardinalDirection.EAST: ">",
    }[direction]


def _directional_button_pairs(
    initial_button: chr, path: tuple[CardinalDirection, ...]
) -> Iterator[tuple[chr, chr]]:
    current_btn = initial_button
    for next_btn in path:
        yield current_btn, _direction_to_btn(next_btn)
        current_btn = _direction_to_btn(next_btn)
    yield current_btn, initial_button


@dataclass(frozen=True)
class _MemoizedId:
    button_pair: tuple[chr, chr]
    num_robots: int


def _min_presses_between_button_pair(
    button_pair: tuple[chr, chr],
    keypad_layout: KeypadLayout,
    directional_robots: KeypadRobots,
    memoized_results: dict[_MemoizedId, int],
) -> int:
    if directional_robots.num_robots < 0:
        return 1
    memoized_id = _MemoizedId(button_pair, directional_robots.num_robots)
    if memoized_id not in memoized_results:
        memoized_results[memoized_id] = _calculate_min_presses(
            button_pair, keypad_layout, directional_robots, memoized_results
        )
    return memoized_results[memoized_id]


def _calculate_min_presses(
    button_pair: tuple[chr, chr],
    keypad_layout: KeypadLayout,
    directional_robots: KeypadRobots,
    memoized_results: dict[_MemoizedId, int],
) -> int:
    return min(
        _min_presses_for_path(path, directional_robots, memoized_results)
        for path in keypad_layout.shortest_paths_between_buttons(*button_pair)
    )


def _min_presses_for_path(
    path: tuple[CardinalDirection, ...],
    directional_robots: KeypadRobots,
    memoized_results: dict[_MemoizedId, int],
) -> int:
    return sum(
        _min_presses_between_button_pair(
            btn_pair,
            directional_robots.robot.keypad_layout,
            directional_robots.decrement(),
            memoized_results,
        )
        for btn_pair in _directional_button_pairs(
            directional_robots.robot.initial_button, path
        )
    )
