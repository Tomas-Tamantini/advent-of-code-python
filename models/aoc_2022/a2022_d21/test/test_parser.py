from models.common.io import InputFromString

from ..parser import parse_operation_monkeys

input_str = """
    root: A + B
    A: B * C
    B: 3
    C: 2
    """


def test_parse_operation_monkeys():
    monkeys = parse_operation_monkeys(InputFromString(input_str))
    assert len(monkeys) == 4
    assert {m.name for m in monkeys} == {"root", "A", "B", "C"}
    assert {m.evaluate() for m in monkeys} == {9, 6, 3, 2}


def test_parse_operation_monkeys_with_unknown_value():
    monkeys = parse_operation_monkeys(
        InputFromString(input_str), monkey_with_unknown_value="C"
    )

    unknown = next(m for m in monkeys if m.name == "C")
    assert unknown.rational_function.numerator.coefficients == (0, 1)
    assert unknown.rational_function.denominator.coefficients == (1,)

    root = next(m for m in monkeys if m.name == "root")
    assert root.solve_for_equality() == 1
