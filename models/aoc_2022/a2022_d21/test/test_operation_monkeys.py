from ..operation_monkeys import LeafMonkey, BinaryOperationMonkey


def test_leaf_monkey_evaluates_to_value_itself():
    leaf = LeafMonkey(name="leaf", value=42)
    assert leaf.evaluate() == 42


def test_binary_operation_monkey_performs_operation_with_left_and_right_child():
    left_child = LeafMonkey(name="left", value=2)
    right_child = LeafMonkey(name="right", value=3)
    operation = lambda x, y: x + y
    binary_operation = BinaryOperationMonkey(left_child, right_child, operation)
    assert binary_operation.evaluate() == 5
