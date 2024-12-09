from dataclasses import dataclass


@dataclass(frozen=True)
class DiskFile:
    file_id: int
    start_address: int
    size: int
