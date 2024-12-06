from models.common.io import InputReader

from .turing_machine import TuringRule, TuringState


def parse_turing_machine_specs(
    input_reader: InputReader,
) -> tuple[str, int, dict[TuringState, TuringRule]]:
    lines = list(input_reader.readlines())
    initial_state = lines[0].strip().split()[-1].replace(".", "")
    steps = int(lines[1].strip().split()[-2])
    transition_rules = {}
    for i in range(3, len(lines), 10):
        state_id = lines[i].strip().split()[-1].replace(":", "")
        current_value = int(lines[i + 1].strip().split()[-1].replace(":", ""))
        write_value = int(lines[i + 2].strip().split()[-1].replace(".", ""))
        move = 1 if "right" in lines[i + 3] else -1
        next_state_id = lines[i + 4].strip().split()[-1].replace(".", "")
        transition_rules[TuringState(state_id, current_value)] = TuringRule(
            next_state_id, write_value, move
        )
        current_value = int(lines[i + 5].strip().split()[-1].replace(":", ""))
        write_value = int(lines[i + 6].strip().split()[-1].replace(".", ""))
        move = 1 if "right" in lines[i + 7] else -1
        next_state_id = lines[i + 8].strip().split()[-1].replace(".", "")
        transition_rules[TuringState(state_id, current_value)] = TuringRule(
            next_state_id, write_value, move
        )
    return initial_state, steps, transition_rules
