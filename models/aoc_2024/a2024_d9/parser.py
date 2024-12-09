from typing import Iterator

from models.common.io import InputReader

from .logic import Disk, DiskFile


def _disk_mapper_sections(content: str) -> Iterator[tuple[int, int]]:
    for i in range(0, len(content), 2):
        section = content[i : i + 2]
        file_size = int(section[0])
        free_space = int(section[1]) if len(section) == 2 else 0
        yield file_size, free_space


def _parse_files(content: str) -> Iterator[DiskFile]:
    current_address = 0
    current_file_id = 0
    for file_size, free_space in _disk_mapper_sections(content):
        yield DiskFile(current_file_id, current_address, file_size)
        current_file_id += 1
        current_address += file_size + free_space


def parse_disk(input_reader: InputReader) -> Disk:
    files = set(_parse_files(input_reader.read()))
    return Disk(files)
