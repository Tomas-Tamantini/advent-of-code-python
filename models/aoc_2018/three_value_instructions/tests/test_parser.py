from models.common.io import InputFromString
from ..parser import parse_three_value_instructions
from ..instructions import (
    AddRegisters,
    AddImmediate,
    MultiplyRegisters,
    MultiplyImmediate,
    BitwiseAndRegisters,
    BitwiseAndImmediate,
    BitwiseOrRegisters,
    BitwiseOrImmediate,
    AssignmentRegisters,
    AssignmentImmediate,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
)


def test_parse_three_value_instructions():
    file_content = """#ip 3
                      addr 10 20 30
                      addi 10 20 30
                      mulr 10 20 30
                      muli 10 20 30
                      banr 10 20 30
                      bani 10 20 30
                      borr 10 20 30
                      bori 10 20 30
                      setr 10 20 30
                      seti 10 20 30
                      gtir 10 20 30
                      gtri 10 20 30
                      gtrr 10 20 30
                      eqir 10 20 30
                      eqri 10 20 30
                      eqrr 10 20 30"""
    expected_types = [
        AddRegisters,
        AddImmediate,
        MultiplyRegisters,
        MultiplyImmediate,
        BitwiseAndRegisters,
        BitwiseAndImmediate,
        BitwiseOrRegisters,
        BitwiseOrImmediate,
        AssignmentRegisters,
        AssignmentImmediate,
        GreaterThanImmediateRegister,
        GreaterThanRegisterImmediate,
        GreaterThanRegisterRegister,
        EqualImmediateRegister,
        EqualRegisterImmediate,
        EqualRegisterRegister,
    ]
    for i, instruction in enumerate(
        parse_three_value_instructions(InputFromString(file_content))
    ):
        assert isinstance(instruction, expected_types[i])
        assert instruction._input_a.value == 10
        assert instruction._input_b.value == 20
        assert instruction._register_out == 30
        assert instruction._register_bound_to_pc == 3
