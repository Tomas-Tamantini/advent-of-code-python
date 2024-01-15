from copy import deepcopy
from .assembunny import Processor, Program, Computer


def run_self_referential_code(program: Program, initial_value: int) -> int:
    copied_program = deepcopy(program)
    computer = Computer(Processor(registers={"a": initial_value}))
    computer.run(copied_program, optimize_assembunny_code=True)
    return computer.value_at("a")
