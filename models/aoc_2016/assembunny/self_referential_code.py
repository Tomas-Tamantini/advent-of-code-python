from copy import deepcopy

from models.common.assembly import Computer, Hardware, Processor

from .program import AssembunnyProgram


def run_self_referential_code(program: AssembunnyProgram, initial_value: int) -> int:
    copied_program = deepcopy(program)
    copied_program.optimize()
    processor = Processor(registers={"a": initial_value})
    hardware = Hardware(processor=processor, memory=copied_program)
    computer = Computer(hardware)
    computer.run_program(copied_program)
    return computer.get_register_value("a")
