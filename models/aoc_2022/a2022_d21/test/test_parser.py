from models.common.io import InputFromString
from ..parser import parse_operation_monkeys


def test_parse_operation_monkeys():
    input_str = """
    root: A + B
    A: B * C
    B: 3
    C: 2
    """

    monkeys = parse_operation_monkeys(InputFromString(input_str))
    assert len(monkeys) == 4
    assert {m.name for m in monkeys} == {"root", "A", "B", "C"}
    assert {m.evaluate() for m in monkeys} == {9, 6, 3, 2}
