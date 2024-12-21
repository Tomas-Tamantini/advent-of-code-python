from math import inf

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
    for i, next_btn in enumerate(code):
        current_btn = code[i - 1] if i > 0 else code_robot.initial_button
        total_length += _min_presses_between_button_pair(
            current_btn,
            next_btn,
            code_robot.keypad_layout,
            directional_robot,
            num_directional_robots,
        )
    return total_length


def _direction_to_btn(direction: CardinalDirection) -> chr:
    if direction == CardinalDirection.NORTH:
        return "^"
    elif direction == CardinalDirection.SOUTH:
        return "v"
    elif direction == CardinalDirection.WEST:
        return "<"
    elif direction == CardinalDirection.EAST:
        return ">"
    else:
        raise ValueError(f"Invalid direction: {direction}")


def _min_presses_between_button_pair(
    current_btn: chr,
    next_btn: chr,
    keypad_layout: KeypadLayout,
    directional_robot: KeypadRobot,
    num_directional_robots: int,
) -> int:
    if num_directional_robots < 0:
        return 1
    else:
        min_num_presses = inf
        for path in keypad_layout.shortest_paths_between_buttons(current_btn, next_btn):
            num_presses = 0
            for i, next_step in enumerate(path):
                current_step = (
                    _direction_to_btn(path[i - 1])
                    if i > 0
                    else directional_robot.initial_button
                )

                num_presses += _min_presses_between_button_pair(
                    current_step,
                    _direction_to_btn(next_step),
                    directional_robot.keypad_layout,
                    directional_robot,
                    num_directional_robots - 1,
                )
            current_step = (
                _direction_to_btn(path[-1])
                if path
                else directional_robot.initial_button
            )
            num_presses += _min_presses_between_button_pair(
                current_step,
                directional_robot.initial_button,
                directional_robot.keypad_layout,
                directional_robot,
                num_directional_robots - 1,
            )
            min_num_presses = min(min_num_presses, num_presses)
        return min_num_presses
