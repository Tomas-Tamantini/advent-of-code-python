from models.common.io import InputFromString
from models.common.assembly import (
    CopyInstruction,
    JumpNotZeroInstruction,
    OutInstruction,
)
from models.aoc_2016.assembunny import (
    parse_assembunny_code,
    DecrementInstruction,
    IncrementInstruction,
    ToggleInstruction,
)


def test_parse_assembunny_code():
    file_content = """cpy 41 a
                      inc b
                      dec c
                      jnz a 2
                      tgl c
                      out d"""
    program = parse_assembunny_code(InputFromString(file_content))
    assert program.get_instruction(0) == CopyInstruction(41, "a")
    assert program.get_instruction(1) == IncrementInstruction("b")
    assert program.get_instruction(2) == DecrementInstruction("c")
    assert program.get_instruction(3) == JumpNotZeroInstruction(
        value_to_compare="a", offset=2
    )
    assert program.get_instruction(4) == ToggleInstruction("c")
    assert program.get_instruction(5) == OutInstruction("d")
