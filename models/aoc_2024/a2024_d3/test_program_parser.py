from .logic import parse_program, MultiplicationOperation


def test_program_parser_parses_multiplication_operations():
    program = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))mul(1234,2)+mul(1, 1)"
    operations = list(parse_program(program))
    assert operations == [
        MultiplicationOperation(2, 4),
        MultiplicationOperation(5, 5),
        MultiplicationOperation(11, 8),
        MultiplicationOperation(8, 5),
    ]
