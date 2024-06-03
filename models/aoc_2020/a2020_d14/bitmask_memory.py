from dataclasses import dataclass
from collections import defaultdict
from typing import Protocol, Optional, Iterator


@dataclass(frozen=True)
class Bitmask:
    mask: str

    def apply(self, value: int) -> int:
        return (value | int(self.mask.replace("X", "0"), base=2)) & int(
            self.mask.replace("X", "1"), base=2
        )


@dataclass(frozen=True)
class FloatingBitmask:
    mask: str

    @property
    def _num_bits(self) -> int:
        return len(self.mask)

    @staticmethod
    def _overwrite_bit(value_as_str: str, bit_idx: int, new_bit: str) -> str:
        return value_as_str[:bit_idx] + new_bit + value_as_str[bit_idx + 1 :]

    def _apply_recursive(
        self, value_as_str: str, current_bit_idx: int
    ) -> Iterator[int]:
        if current_bit_idx == len(self.mask):
            yield int(value_as_str, base=2)
            return

        if self.mask[current_bit_idx] == "0":
            yield from self._apply_recursive(value_as_str, current_bit_idx + 1)
        elif self.mask[current_bit_idx] == "1":
            new_value = self._overwrite_bit(value_as_str, current_bit_idx, "1")
            yield from self._apply_recursive(new_value, current_bit_idx + 1)
        elif self.mask[current_bit_idx] == "X":
            new_value = self._overwrite_bit(value_as_str, current_bit_idx, "0")
            yield from self._apply_recursive(new_value, current_bit_idx + 1)

            new_value = self._overwrite_bit(value_as_str, current_bit_idx, "1")
            yield from self._apply_recursive(new_value, current_bit_idx + 1)
        else:
            raise ValueError(f"Invalid mask bit: {self.mask[current_bit_idx]}")

    def apply(self, value: int) -> Iterator[int]:
        value_as_str = format(value, f"0{self._num_bits}b")
        return self._apply_recursive(value_as_str, current_bit_idx=0)


class BitmaskMemory:
    def __init__(
        self,
        value_mask: Optional[Bitmask] = None,
        address_mask: Optional[FloatingBitmask] = None,
    ) -> None:
        self._value_mask = value_mask
        self._address_mask = address_mask
        self._stored_values = defaultdict(int)

    def update_value_mask(self, mask: Bitmask) -> None:
        self._value_mask = mask

    def update_address_mask(self, mask: FloatingBitmask) -> None:
        self._address_mask = mask

    def _transformed_addresses(self, address: int) -> Iterator[int]:
        if self._address_mask is None:
            yield address
        else:
            yield from self._address_mask.apply(address)

    def store(self, address: int, value: int) -> None:
        transformed_value = (
            value if self._value_mask is None else self._value_mask.apply(value)
        )
        for transformed_address in self._transformed_addresses(address):
            self._stored_values[transformed_address] = transformed_value

    def sum_values(self) -> int:
        return sum(self._stored_values.values())


class BitmaskInstruction(Protocol):
    def execute(self, memory: BitmaskMemory) -> None: ...


@dataclass(frozen=True)
class SetMaskInstruction:
    mask: str
    is_address_mask: bool

    def execute(self, memory: BitmaskMemory) -> None:
        if self.is_address_mask:
            memory.update_address_mask(FloatingBitmask(self.mask))
        else:
            memory.update_value_mask(Bitmask(self.mask))


@dataclass(frozen=True)
class WriteToMemoryInstruction:
    address: int
    value: int

    def execute(self, memory: BitmaskMemory) -> None:
        memory.store(self.address, self.value)
