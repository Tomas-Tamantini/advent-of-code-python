from models.common.io import InputFromString

from ..logic import Equation
from ..parser import parse_equations


def test_parse_equations():
    file_content = """190: 10 19
                      3267: 81 40 27"""
    input_reader = InputFromString(file_content)
    equations = list(parse_equations(input_reader))
    assert equations == [
        Equation(test_value=190, terms=(10, 19)),
        Equation(test_value=3267, terms=(81, 40, 27)),
    ]
