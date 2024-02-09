from models.assembly import Hardware, Processor, Computer
from .intcode import IntcodeProgram


def run_intcode_program_until_halt(sequence: list[int]) -> list[int]:
    program = IntcodeProgram(sequence[:])
    hardware = Hardware(processor=Processor(), memory=program)
    computer = Computer(hardware)
    computer.run_program(program)
    return program.sequence
