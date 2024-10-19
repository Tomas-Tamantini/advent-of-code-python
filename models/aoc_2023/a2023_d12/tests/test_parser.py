from models.common.io import InputFromString
from ..logic import NonogramRow
from ..parser import parse_nonogram_rows

_FILE_CONTENT = """???.### 1,1,3
                   ?#?#?#?#?#?#?#? 1,3,1,6"""


def test_nonogram_rows_can_be_parsed_with_single_repetition():
    input_reader = InputFromString(_FILE_CONTENT)
    rows = list(parse_nonogram_rows(input_reader, number_of_repetitions=1))
    assert rows == [
        NonogramRow(cells="???.###", contiguous_groups_sizes=(1, 1, 3)),
        NonogramRow(cells="?#?#?#?#?#?#?#?", contiguous_groups_sizes=(1, 3, 1, 6)),
    ]


def test_nonogram_rows_can_be_parsed_with_repetitions_spaced_by_question_mark():
    input_reader = InputFromString(_FILE_CONTENT)
    rows = list(parse_nonogram_rows(input_reader, number_of_repetitions=3))
    assert rows == [
        NonogramRow(
            cells="???.###????.###????.###",
            contiguous_groups_sizes=(1, 1, 3, 1, 1, 3, 1, 1, 3),
        ),
        NonogramRow(
            cells="?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#?",
            contiguous_groups_sizes=(1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6),
        ),
    ]
