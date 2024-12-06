from models.common.io import InputFromString

from ..parser import parse_code_row_and_col


def test_parse_code_row_and_column():
    file_content = "To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019."
    row_and_col = parse_code_row_and_col(InputFromString(file_content))
    assert row_and_col == {"row": 3010, "col": 3019}
