from copy import deepcopy
from models.assembly import Processor
from models.aoc_2016.assembunny import (
    Computer,
    Program,
    CopyInstruction,
    IncrementInstruction,
    DecrementInstruction,
    JumpNotZeroInstruction,
    ToggleInstruction,
)


def test_computer_can_run_simple_program():
    simple_program = Program(
        [
            CopyInstruction(41, "a"),
            IncrementInstruction("a"),
            IncrementInstruction("a"),
            DecrementInstruction("a"),
            JumpNotZeroInstruction("a", 2),
            DecrementInstruction("a"),
        ]
    )
    computer = Computer(Processor())

    computer.run(simple_program, optimize_assembunny_code=False)
    assert computer.value_at("a") == 42


def test_computer_can_run_fibonacci_like_program_efficiently():
    fibonacci_program = Program(
        [
            CopyInstruction(1, "a"),
            CopyInstruction(1, "b"),
            CopyInstruction(26, "d"),
            JumpNotZeroInstruction("c", 2),
            JumpNotZeroInstruction(1, 5),
            CopyInstruction(7, "c"),
            IncrementInstruction("d"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction("c", -2),
            CopyInstruction("a", "c"),
            IncrementInstruction("a"),
            DecrementInstruction("b"),
            JumpNotZeroInstruction("b", -2),
            CopyInstruction("c", "b"),
            DecrementInstruction("d"),
            JumpNotZeroInstruction("d", -6),
            CopyInstruction(16, "c"),
            CopyInstruction(17, "d"),
            IncrementInstruction("a"),
            DecrementInstruction("d"),
            JumpNotZeroInstruction("d", -2),
            DecrementInstruction("c"),
            JumpNotZeroInstruction("c", -5),
        ]
    )

    computer = Computer(Processor())
    computer.run(fibonacci_program, optimize_assembunny_code=True)
    assert computer.value_at("a") == 318083

    computer = Computer(Processor(registers={"c": 1}))
    computer.run(fibonacci_program, optimize_assembunny_code=True)
    assert computer.value_at("a") == 9227737


def test_computer_can_run_factorial_like_program_efficiently():
    factorial_program = Program(
        [
            CopyInstruction("a", "b"),
            DecrementInstruction("b"),
            CopyInstruction("a", "d"),
            CopyInstruction(0, "a"),
            CopyInstruction("b", "c"),
            IncrementInstruction("a"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction("c", -2),
            DecrementInstruction("d"),
            JumpNotZeroInstruction("d", -5),
            DecrementInstruction("b"),
            CopyInstruction("b", "c"),
            CopyInstruction("c", "d"),
            DecrementInstruction("d"),
            IncrementInstruction("c"),
            JumpNotZeroInstruction("d", -2),
            ToggleInstruction("c"),
            CopyInstruction(-16, "c"),
            JumpNotZeroInstruction(1, "c"),
            CopyInstruction(86, "c"),
            JumpNotZeroInstruction(78, "d"),
            IncrementInstruction("a"),
            IncrementInstruction("d"),
            JumpNotZeroInstruction("d", -2),
            IncrementInstruction("c"),
            JumpNotZeroInstruction("c", -5),
        ]
    )

    computer = Computer(Processor({"a": 7}))
    computer.run(deepcopy(factorial_program), optimize_assembunny_code=True)
    assert computer.value_at("a") == 11748

    computer = Computer(Processor({"a": 12}))
    computer.run(factorial_program, optimize_assembunny_code=True)
    assert computer.value_at("a") == 479008308
