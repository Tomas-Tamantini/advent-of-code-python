from ..logic import Equation


def test_equation_combines_first_two_terms():
    equation = Equation(test_value=190, terms=(10, 19))
    new_equation = equation.apply_operator_to_first_pair(lambda x, y: x + y)
    assert new_equation == Equation(test_value=190, terms=(29,))
