from models.common.io import InputFromString
from ..parser import parse_string_transformers
from ..string_transform import Spin, Exchange, Partner


def test_parse_string_transformers():
    file_content = "s1,x0/12, pb/X"
    transformers = list(parse_string_transformers(InputFromString(file_content)))
    assert transformers == [Spin(1), Exchange(0, 12), Partner("b", "X")]
