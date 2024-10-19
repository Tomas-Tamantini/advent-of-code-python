from models.common.io import InputFromString
from ..parser import parse_initialization_steps
from ..logic import InsertLens, RemoveLens


def test_parse_initialization_sequence():
    file_content = "xpb=9,rds-"
    input_reader = InputFromString(file_content)
    steps = list(parse_initialization_steps(input_reader))
    assert steps == [InsertLens("xpb", focal_strength=9), RemoveLens("rds")]
