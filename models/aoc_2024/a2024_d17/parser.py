from models.common.io import InputReader


def parse_3_bit_program(input_reader: InputReader) -> tuple[int, ...]:
    for line in input_reader.read_stripped_lines():
        if "Program" in line:
            return tuple(map(int, line.split(":")[1].split(",")))


def parse_3_bit_registers(input_reader: InputReader) -> dict[chr, int]:
    registers = dict()
    for line in input_reader.read_stripped_lines():
        if "Register" in line:
            register, value = line.split(":")
            registers[register.split()[1]] = int(value)
    return registers
