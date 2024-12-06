from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(frozen=True)
class File:
    name: str
    size: int


class _Directory:
    def __init__(self, name: str, parent: Optional["_Directory"] = None) -> None:
        self._name = name
        self._files = []
        self._subdirectories = []
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    def add_file(self, file: File) -> None:
        if any(f.name == file.name for f in self._files):
            raise ValueError(f"File with name {file.name} already exists in directory")
        self._files.append(file)

    def add_subdirectory(self, directory: "_Directory") -> None:
        if any(d.name == directory.name for d in self._subdirectories):
            raise ValueError(
                f"Subdirectory with name {directory.name} already exists in directory"
            )
        self._subdirectories.append(directory)

    def size(self) -> int:
        return sum(f.size for f in self._files) + sum(
            d.size() for d in self._subdirectories
        )

    def navigate_to_subdirectory(self, name: str) -> "_Directory":
        for subdir in self._subdirectories:
            if subdir.name == name:
                return subdir
        raise ValueError(f"Subdirectory with name {name} does not exist in directory")

    def all_directories(self) -> Iterator["_Directory"]:
        yield self
        for subdir in self._subdirectories:
            yield from subdir.all_directories()


class FileTree:
    def __init__(self) -> None:
        self._root = _Directory(name="/")
        self._current_directory = self._root

    @property
    def current_directory(self) -> _Directory:
        return self._current_directory

    def add_file(self, file: File) -> None:
        self._current_directory.add_file(file)

    def add_directory(self, name: str) -> None:
        new_dir = _Directory(name, parent=self._current_directory)
        self._current_directory.add_subdirectory(new_dir)

    def navigate_to_subdirectory(self, name: str) -> None:
        self._current_directory = self._current_directory.navigate_to_subdirectory(name)

    def navigate_to_parent_directory(self) -> None:
        if self._current_directory == self._root:
            return
        self._current_directory = self._current_directory._parent

    def navigate_to_root(self) -> None:
        self._current_directory = self._root

    def all_directories(self) -> Iterator[_Directory]:
        return self._root.all_directories()
