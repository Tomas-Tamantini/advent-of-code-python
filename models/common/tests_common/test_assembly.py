from unittest.mock import Mock

import pytest

from models.common.assembly import (
    Computer,
    ContextFreeGrammar,
    Hardware,
    ImmutableProgram,
    Processor,
    Program,
)


def test_hardware_can_have_custom_attributes():
    hardware = Hardware(processor=Processor(), custom_attr=123)
    assert hardware.custom_attr == 123
    hardware.custom_attr = 456
    assert hardware.custom_attr == 456


def test_computer_can_be_initialized_from_processor():
    processor = Processor(registers={"a": 1, "b": 2})
    computer = Computer.from_processor(processor)
    assert computer.get_register_value("a") == 1
    assert computer.get_register_value("b") == 2


def test_running_program_with_no_instructions_does_nothing():
    processor = Processor(registers={"a": 1, "b": 2})
    computer = Computer.from_processor(processor)
    empty_program = Mock(spec=Program)
    empty_program.get_instruction.return_value = None
    computer.run_program(empty_program)
    assert computer.get_register_value("a") == 1
    assert computer.get_register_value("b") == 2


def test_program_instructions_are_executed_until_end_of_program():
    class SerialOutputSpy:
        def __init__(self):
            self.output = []

        def write(self, value):
            self.output.append(value)

    class IncrementInstruction:
        @staticmethod
        def execute(hardware):
            hardware.processor.registers["a"] += (
                hardware.processor.get_value_or_immediate("b")
            )
            hardware.increment_program_counter()

    class OutputInstruction:
        @staticmethod
        def execute(hardware):
            hardware.serial_output.write(hardware.processor.registers["a"])
            if hardware.processor.get_value_or_immediate("a") >= 9:
                hardware.increment_program_counter()
            else:
                hardware.increment_program_counter(increment=-1)

    program = ImmutableProgram([IncrementInstruction(), OutputInstruction()])

    processor = Processor(registers={"a": 1, "b": 2})
    serial_output = SerialOutputSpy()
    computer = Computer(
        hardware=Hardware(processor=processor, serial_output=serial_output)
    )
    computer.run_program(program)
    assert computer.get_register_value("a") == 9
    assert serial_output.output == [3, 5, 7, 9]


def test_can_execute_instructions_one_by_one():
    class NoOpInstruction:
        @staticmethod
        def execute(hardware):
            hardware.increment_program_counter()

    program = ImmutableProgram([NoOpInstruction(), NoOpInstruction()])
    processor = Processor()
    computer = Computer.from_processor(processor)
    computer.run_next_instruction(program)
    assert computer._program_counter == 1
    computer.run_next_instruction(program)
    assert computer._program_counter == 2
    with pytest.raises(StopIteration):
        computer.run_next_instruction(program)


def test_context_free_grammar_with_single_rule_matches_single_token():
    grammar = ContextFreeGrammar(starting_symbol="S")
    grammar.add_rule(symbol="S", production=("a",))
    assert grammar.matches(("a",))
    assert not grammar.matches(("b",))


def test_adding_rules_to_the_same_symbol_results_in_union_in_context_free_grammar():
    grammar = ContextFreeGrammar(starting_symbol="S")
    grammar.add_rule("S", ("a",))
    grammar.add_rule("S", ("b",))
    assert grammar.matches(("a",))
    assert grammar.matches(("b",))
    assert not grammar.matches(("c",))
    assert not grammar.matches(("a", "b"))


def test_context_free_grammar_can_have_recursive_rules():
    grammar = ContextFreeGrammar(starting_symbol=0)
    grammar.add_rule(0, (1, 2))
    grammar.add_rule(1, ("a",))
    grammar.add_rule(2, (1, 3))
    grammar.add_rule(2, (3, 1))
    grammar.add_rule(3, ("b",))
    assert grammar.matches(tuple("aab"))
    assert grammar.matches(tuple("aba"))
    assert not grammar.matches(tuple("aaa"))
    assert not grammar.matches(tuple("bbb"))
    assert not grammar.matches(tuple("abb"))
    assert not grammar.matches(tuple("bab"))

    grammar = ContextFreeGrammar(starting_symbol=0)
    grammar.add_rule(0, (4, 1, 5))
    grammar.add_rule(1, (2, 3))
    grammar.add_rule(1, (3, 2))
    grammar.add_rule(2, (4, 4))
    grammar.add_rule(2, (5, 5))
    grammar.add_rule(3, (4, 5))
    grammar.add_rule(3, (5, 4))
    grammar.add_rule(4, ("a",))
    grammar.add_rule(5, ("b",))
    assert grammar.matches(tuple("aaaabb"))
    assert grammar.matches(tuple("abbabb"))
    assert grammar.matches(tuple("aabaab"))
    assert grammar.matches(tuple("ababbb"))
    assert not grammar.matches(tuple("bababa"))
    assert not grammar.matches(tuple("aaabbb"))
    assert not grammar.matches(tuple("aaaabbb"))


def test_context_free_grammar_can_have_self_referencing_rules():
    grammar = ContextFreeGrammar(starting_symbol="A")
    grammar.add_rule("A", ("a", "A", "b"))
    grammar.add_rule("A", ("c",))
    assert grammar.matches(tuple("c"))
    assert grammar.matches(tuple("acb"))
    assert grammar.matches(tuple("aacbb"))
