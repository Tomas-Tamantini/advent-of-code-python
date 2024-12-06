from .instructions import (
    ALL_THREE_VALUE_INSTRUCTIONS,
    AddImmediate,
    AddRegisters,
    AssignmentImmediate,
    AssignmentRegisters,
    BitwiseAndImmediate,
    BitwiseAndRegisters,
    BitwiseOrImmediate,
    BitwiseOrRegisters,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    MultiplyImmediate,
    MultiplyRegisters,
    ThreeValueInstruction,
)
from .parser import parse_three_value_instructions
