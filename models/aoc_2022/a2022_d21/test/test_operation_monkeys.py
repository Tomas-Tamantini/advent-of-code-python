from models.common.polynomials import RationalFunction, Polynomial
from ..operation_monkeys import LeafMonkey, BinaryOperationMonkey


def test_leaf_monkey_substitutes_x_for_zero_in_its_evaluation():
    leaf = LeafMonkey(
        name="leaf",
        rational_function=RationalFunction(
            numerator=Polynomial((84, 3, 11)), denominator=Polynomial((2, 7))
        ),
    )
    assert leaf.evaluate() == 42


def test_binary_operation_monkey_performs_operation_with_left_and_right_child():
    left_child = LeafMonkey(
        name="left",
        rational_function=RationalFunction(
            numerator=Polynomial((2,)), denominator=Polynomial((1,))
        ),
    )
    right_child = LeafMonkey(
        name="right",
        rational_function=RationalFunction(
            numerator=Polynomial((3,)), denominator=Polynomial((1,))
        ),
    )
    operation = lambda x, y: x + y
    binary_operation = BinaryOperationMonkey(
        "binary", left_child, right_child, operation
    )
    assert binary_operation.evaluate() == 5
