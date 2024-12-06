from ..logic import (
    DoInstruction,
    DontInstruction,
    MultiplicationInstruction,
    parse_program,
)


def test_program_parser_parses_multiplication_instructions():
    program = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))mul(1234,2)+mul(1, 1)"
    instructions = list(parse_program(program))
    assert instructions == [
        MultiplicationInstruction(2, 4),
        MultiplicationInstruction(5, 5),
        MultiplicationInstruction(11, 8),
        MultiplicationInstruction(8, 5),
    ]


def test_program_parser_parses_dos_and_donts_instructions():
    program = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    instructions = list(parse_program(program))
    assert instructions == [
        MultiplicationInstruction(2, 4),
        DontInstruction(),
        MultiplicationInstruction(5, 5),
        MultiplicationInstruction(11, 8),
        DoInstruction(),
        MultiplicationInstruction(8, 5),
    ]
