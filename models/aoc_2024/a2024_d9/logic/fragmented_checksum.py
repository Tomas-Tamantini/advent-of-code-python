from dataclasses import dataclass
from typing import Iterable, Iterator

from .disk_file import DiskFile


@dataclass(frozen=True, order=True)
class _FilePointer:
    file_index: int
    offset: int

    def current_file(self, files: list[DiskFile]) -> DiskFile:
        return files[self.file_index]

    def absolute_address(self, files: list[DiskFile]) -> int:
        return self.current_file(files).start_address + self.offset

    def increment(self, files: list[DiskFile]) -> "_FilePointer":
        if self.offset + 1 < self.current_file(files).size:
            return _FilePointer(file_index=self.file_index, offset=self.offset + 1)
        else:
            return _FilePointer(file_index=self.file_index + 1, offset=0)

    def decrement(self, files: list[DiskFile]) -> "_FilePointer":
        if self.offset - 1 >= 0:
            return _FilePointer(file_index=self.file_index, offset=self.offset - 1)
        else:
            return _FilePointer(
                file_index=self.file_index - 1,
                offset=files[self.file_index - 1].size - 1,
            )


def _compacted_files(sorted_files: list[DiskFile]) -> Iterator[int]:
    left_pointer = _FilePointer(file_index=0, offset=0)
    right_pointer = _FilePointer(
        file_index=len(sorted_files) - 1, offset=sorted_files[-1].size - 1
    )
    current_address = 0
    while left_pointer <= right_pointer:
        left_address = left_pointer.absolute_address(sorted_files)
        if left_address == current_address:
            yield left_pointer.current_file(sorted_files).file_id
            left_pointer = left_pointer.increment(sorted_files)
        else:
            yield right_pointer.current_file(sorted_files).file_id
            right_pointer = right_pointer.decrement(sorted_files)
        current_address += 1


def fragmented_checksum(files: Iterable[DiskFile]) -> int:
    sorted_files = sorted(files, key=lambda f: f.start_address)
    return sum(i * file_id for i, file_id in enumerate(_compacted_files(sorted_files)))
