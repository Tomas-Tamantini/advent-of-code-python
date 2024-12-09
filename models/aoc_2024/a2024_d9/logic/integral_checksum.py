from dataclasses import dataclass
from typing import Iterable, Iterator

from .disk_file import DiskFile


@dataclass(frozen=True)
class _EmptySpace:
    start_address: int
    size: int

    def allocate(self, disk_file: DiskFile) -> tuple[DiskFile, "_EmptySpace"]:
        new_file = DiskFile(disk_file.file_id, self.start_address, disk_file.size)
        new_empty_space = _EmptySpace(
            self.start_address + disk_file.size, self.size - disk_file.size
        )
        return new_file, new_empty_space


class _IntegralChecksumCalculator:
    def __init__(self, files: Iterable[DiskFile]):
        self._files = sorted(files, key=lambda f: f.start_address)
        self._file_indices = {disk_file: i for i, disk_file in enumerate(self._files)}
        self._empty_spaces = list(self._generate_empty_spaces())
        self._allocate_empty_spaces()

    def _allocate_empty_spaces(self) -> None:
        for disk_file in reversed(self._files):
            index_of_empty_space = self._index_of_first_empty_space_that_fits(disk_file)
            if index_of_empty_space >= 0:
                self._allocate_file_to_empty_space(disk_file, index_of_empty_space)

    def _allocate_file_to_empty_space(
        self, disk_file: DiskFile, index_of_empty_space: int
    ) -> None:
        empty_space = self._empty_spaces[index_of_empty_space]
        new_file, new_empty_space = empty_space.allocate(disk_file)
        self._replace_file(disk_file, new_file)
        if new_empty_space.size > 0:
            self._empty_spaces[index_of_empty_space] = new_empty_space
        else:
            self._empty_spaces.pop(index_of_empty_space)

    def _replace_file(self, old_file: DiskFile, new_file: DiskFile) -> None:
        file_index = self._file_indices[old_file]
        self._file_indices[new_file] = file_index
        del self._file_indices[old_file]
        self._files[file_index] = new_file

    def _generate_empty_spaces(self) -> Iterator[_EmptySpace]:
        for i in range(1, len(self._files)):
            start_address = self._files[i - 1].start_address + self._files[i - 1].size
            end_address = self._files[i].start_address
            size = end_address - start_address
            if size:
                yield _EmptySpace(start_address, size)

    def _index_of_first_empty_space_that_fits(self, disk_file: DiskFile) -> int:
        for i, empty_space in enumerate(self._empty_spaces):
            if empty_space.start_address >= disk_file.start_address:
                return -1
            elif empty_space.size >= disk_file.size:
                return i
        return -1

    @staticmethod
    def _checksum_for_file(file: DiskFile) -> int:
        address_start = file.start_address
        address_end = address_start + file.size
        return file.file_id * sum(range(address_start, address_end))

    def checksum(self) -> int:
        return sum(self._checksum_for_file(file) for file in self._files)


def integral_checksum(files: Iterable[DiskFile]) -> int:
    return _IntegralChecksumCalculator(files).checksum()
