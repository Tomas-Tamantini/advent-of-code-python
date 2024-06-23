from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_cardinal_direction_instructions
from .keypad import Keypad


def aoc_2016_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 2, "Bathroom Security")
    io_handler.output_writer.write_header(problem_id)
    keypad_three_by_three = Keypad(configuration="123\n456\n789", initial_key="5")
    keypad_rhombus = Keypad(
        configuration="**1**\n*234*\n56789\n*ABC*\n**D**", initial_key="5"
    )
    keys_3x3 = []
    keys_rhombus = []
    for instructions in parse_cardinal_direction_instructions(io_handler.input_reader):
        keypad_three_by_three.move_multiple_keys(instructions)
        keys_3x3.append(keypad_three_by_three.key)
        keypad_rhombus.move_multiple_keys(instructions)
        keys_rhombus.append(keypad_rhombus.key)
    solution = ProblemSolution(
        problem_id, f"Bathroom code for 3x3 pad is {''.join(keys_3x3)}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id, f"Bathroom code for rhombus pad is {''.join(keys_rhombus)}", part=2
    )
    io_handler.output_writer.write_solution(solution)
