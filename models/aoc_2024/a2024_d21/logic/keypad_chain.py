from math import inf
from typing import Iterator

from models.common.vectors import CardinalDirection

from .keypad_layout import KeypadLayout
from .keypad_robot import KeypadRobot


def min_num_keypad_presses(
    code: str,
    code_robot: KeypadRobot,
    directional_robot: KeypadRobot,
    num_directional_robots: int,
) -> int:
    total_length = 0
    memoized_results = dict()
    for i, next_btn in enumerate(code):
        current_btn = code[i - 1] if i > 0 else code_robot.initial_button
        total_length += _min_presses_between_button_pair(
            current_btn,
            next_btn,
            code_robot.keypad_layout,
            directional_robot,
            num_directional_robots,
            memoized_results,
        )
    return total_length


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


def _min_presses_between_button_pair(
    current_btn: chr,
    next_btn: chr,
    keypad_layout: KeypadLayout,
    directional_robot: KeypadRobot,
    num_directional_robots: int,
    memoized_results: dict[tuple[chr, chr, int], int],
) -> int:
    if num_directional_robots < 0:
        return 1
    iteration_id = (current_btn, next_btn, num_directional_robots)
    if iteration_id not in memoized_results:
        min_num_presses = inf
        for path in keypad_layout.shortest_paths_between_buttons(current_btn, next_btn):
            num_presses = sum(
                _min_presses_between_button_pair(
                    *btn_pair,
                    directional_robot.keypad_layout,
                    directional_robot,
                    num_directional_robots - 1,
                    memoized_results
                )
                for btn_pair in _directional_button_pairs(
                    directional_robot.initial_button, path
                )
            )
            min_num_presses = min(min_num_presses, num_presses)
        memoized_results[iteration_id] = min_num_presses
    return memoized_results[iteration_id]
