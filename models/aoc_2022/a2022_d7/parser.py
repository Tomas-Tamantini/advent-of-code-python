from typing import Iterator
from models.common.io import InputReader
from .file_tree import FileTree, File


def _non_ls_lines(input_reader: InputReader) -> Iterator[str]:
    for line in input_reader.read_stripped_lines():
        if not line.startswith("$ ls"):
            yield line


def _parse_navigate_command(file_tree: FileTree, argument: str) -> None:
    if argument == "/":
        file_tree.navigate_to_root()
    elif argument == "..":
        file_tree.navigate_to_parent_directory()
    else:
        file_tree.navigate_to_subdirectory(argument)


def _add_component(file_tree: FileTree, line: str) -> None:
    parts = line.split(" ")
    name = parts[-1].strip()
    if parts[0].strip() == "dir":
        file_tree.add_directory(name)
    else:
        file_size = int(parts[0].strip())
        file = File(name, file_size)
        file_tree.add_file(file)


def parse_file_tree(input_reader: InputReader) -> FileTree:
    file_tree = FileTree()
    for line in _non_ls_lines(input_reader):
        if line.startswith("$ cd"):
            _parse_navigate_command(file_tree, argument=line.split(" ")[-1].strip())
        else:
            _add_component(file_tree, line)
    return file_tree
