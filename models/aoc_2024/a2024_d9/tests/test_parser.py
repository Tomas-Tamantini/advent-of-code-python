from models.common.io import InputFromString

from ..logic import DiskFile
from ..parser import parse_disk_files


def test_parse_disk():
    file_content = "12345"
    input_reader = InputFromString(file_content)
    files = list(parse_disk_files(input_reader))
    assert files == [
        DiskFile(file_id=0, start_address=0, size=1),
        DiskFile(file_id=1, start_address=3, size=3),
        DiskFile(file_id=2, start_address=10, size=5),
    ]
