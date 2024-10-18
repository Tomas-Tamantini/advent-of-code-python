from dataclasses import dataclass


@dataclass(frozen=True)
class NonogramRow:
    cells: str
    contiguous_groups_sizes: tuple[int, ...]

    @property
    def num_cells(self) -> int:
        return len(self.cells)

    @property
    def num_groups(self) -> int:
        return len(self.contiguous_groups_sizes)
