from models.common.io import InputFromString

from ..parser import parse_disk


def test_parse_disk():
    file_content = "2333133121414131402"
    input_reader = InputFromString(file_content)
    disk = parse_disk(input_reader)
    assert disk.compacted_checksum() == 1928
