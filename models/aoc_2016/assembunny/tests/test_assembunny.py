from models.aoc_2016.assembunny import (
    AssembunnyProgram,
    DecrementInstruction,
    IncrementInstruction,
    ToggleInstruction,
    run_self_referential_code,
)
from models.common.assembly import (
    Computer,
    CopyInstruction,
    JumpNotZeroInstruction,
    Processor,
)


def test_computer_can_run_simple_program():
    simple_program = AssembunnyProgram(
        [
            CopyInstruction(41, "a"),
            IncrementInstruction("a"),
            IncrementInstruction("a"),
            DecrementInstruction("a"),
            JumpNotZeroInstruction(value_to_compare="a", offset=2),
            DecrementInstruction("a"),
        ]
    )
    computer = Computer.from_processor(Processor())

    computer.run_program(simple_program)
    assert computer.get_register_value("a") == 42


def test_computer_can_run_fibonacci_like_program_efficiently():
    fibonacci_program = AssembunnyProgram(
        [
            CopyInstruction(1, "a"),
            CopyInstruction(1, "b"),
            CopyInstruction(26, "d"),
            JumpNotZeroInstruction(value_to_compare="c", offset=2),
            JumpNotZeroInstruction(value_to_compare=1, offset=5),
            CopyInstruction(7, "c"),
            IncrementInstruction("d"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-2),
            CopyInstruction("a", "c"),
            IncrementInstruction("a"),
            DecrementInstruction("b"),
            JumpNotZeroInstruction(value_to_compare="b", offset=-2),
            CopyInstruction("c", "b"),
            DecrementInstruction("d"),
            JumpNotZeroInstruction(value_to_compare="d", offset=-6),
            CopyInstruction(16, "c"),
            CopyInstruction(17, "d"),
            IncrementInstruction("a"),
            DecrementInstruction("d"),
            JumpNotZeroInstruction(value_to_compare="d", offset=-2),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-5),
        ]
    )
    fibonacci_program.optimize()
    computer = Computer.from_processor(Processor())
    computer.run_program(fibonacci_program)
    assert computer.get_register_value("a") == 318083

    computer = Computer.from_processor(Processor(registers={"c": 1}))
    computer.run_program(fibonacci_program)
    assert computer.get_register_value("a") == 9227737


def test_computer_can_run_factorial_like_program_efficiently():
    factorial_program = AssembunnyProgram(
        [
            CopyInstruction("a", "b"),
            DecrementInstruction("b"),
            CopyInstruction("a", "d"),
            CopyInstruction(0, "a"),
            CopyInstruction("b", "c"),
            IncrementInstruction("a"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-2),
            DecrementInstruction("d"),
            JumpNotZeroInstruction(value_to_compare="d", offset=-5),
            DecrementInstruction("b"),
            CopyInstruction("b", "c"),
            CopyInstruction("c", "d"),
            DecrementInstruction("d"),
            IncrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="d", offset=-2),
            ToggleInstruction("c"),
            CopyInstruction(-16, "c"),
            JumpNotZeroInstruction(value_to_compare=1, offset="c"),
            CopyInstruction(86, "c"),
            JumpNotZeroInstruction(value_to_compare=78, offset="d"),
            IncrementInstruction("a"),
            IncrementInstruction("d"),
            JumpNotZeroInstruction(value_to_compare="d", offset=-2),
            IncrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-5),
        ]
    )
    assert run_self_referential_code(factorial_program, initial_value=7) == 11748
    assert run_self_referential_code(factorial_program, initial_value=12) == 479008308
