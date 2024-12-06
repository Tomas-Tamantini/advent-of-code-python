from typing import Iterator

from models.common.io import InputReader

from .storage_node import StorageNode


def _parse_storage_node(line: str) -> StorageNode:
    parts = line.strip().split()
    return StorageNode(
        id=parts[0].replace("/dev/grid/node-", ""),
        size=int(parts[1].replace("T", "")),
        used=int(parts[2].replace("T", "")),
    )


def parse_storage_nodes(input_reader: InputReader) -> Iterator[StorageNode]:
    for line in input_reader.readlines():
        if "node" in line:
            yield _parse_storage_node(line)
