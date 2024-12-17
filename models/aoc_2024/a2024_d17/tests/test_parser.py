from models.common.io import InputFromString

from ..parser import parse_3_bit_program, parse_3_bit_registers

_FILE_CONTENT = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


def test_parse_3_bit_program():
    input_reader = InputFromString(_FILE_CONTENT)
    program = parse_3_bit_program(input_reader)
    assert (0, 1, 5, 4, 3, 0) == program


def test_parse_3_bit_registers():
    input_reader = InputFromString(_FILE_CONTENT)
    registers = parse_3_bit_registers(input_reader)
    assert {"A": 729, "B": 0, "C": 0} == registers
