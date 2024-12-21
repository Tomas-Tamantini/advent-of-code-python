from .keypad_layout import KeypadLayout
from .keypad_robot import KeypadRobot


def min_num_keypad_presses(code: str, code_robot: KeypadRobot) -> int:
    total_length = 0
    for i, next_btn in enumerate(code):
        current_btn = code[i - 1] if i > 0 else code_robot.initial_button
        total_length += _min_presses_between_code_pair(
            current_btn, next_btn, code_robot.keypad_layout
        )
    return total_length


def _min_presses_between_code_pair(
    current_btn: chr, next_btn: chr, code_keypad_layout: KeypadLayout
) -> int:
    if current_btn == next_btn:
        return 1
    else:
        shortest_path = next(
            code_keypad_layout.shortest_paths_between_buttons(current_btn, next_btn)
        )
        return len(shortest_path) + 1
