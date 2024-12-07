import pytest

from ..logic import Equation, is_valid_equation


@pytest.mark.parametrize(
    "valid_equation",
    [
        Equation(test_value=190, terms=(10, 19)),
        Equation(test_value=3267, terms=(81, 40, 27)),
        Equation(test_value=292, terms=(11, 6, 16, 20)),
    ],
)
def test_equation_is_valid_if_some_combination_of_operators_produces_test_value(
    valid_equation,
):
    assert is_valid_equation(
        valid_equation, possible_operators=(lambda x, y: x + y, lambda x, y: x * y)
    )


@pytest.mark.parametrize(
    "invalid_equation",
    [
        Equation(test_value=83, terms=(17, 5)),
        Equation(test_value=156, terms=(15, 6)),
        Equation(test_value=7290, terms=(6, 8, 6, 15)),
        Equation(test_value=161011, terms=(16, 10, 13)),
        Equation(test_value=192, terms=(17, 8, 14)),
        Equation(test_value=21037, terms=(9, 7, 18, 13)),
    ],
)
def test_equation_is_invalid_if_no_combination_of_operators_produces_test_value(
    invalid_equation,
):
    assert not is_valid_equation(
        invalid_equation, possible_operators=(lambda x, y: x + y, lambda x, y: x * y)
    )
