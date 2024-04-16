from unittest.mock import Mock
from models.aoc_2020 import (
    Bitmask,
    BitmaskMemory,
    SetMaskInstruction,
    WriteToMemoryInstruction,
)

mask = Bitmask(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")


def test_bitmask_overwrites_bits_in_value():
    assert mask.apply(11) == 73
    assert mask.apply(101) == 101
    assert mask.apply(0) == 64


def test_bitmask_memory_starts_empty():
    memory = BitmaskMemory(mask)
    assert memory.sum_values() == 0


def test_bitmask_memory_transforms_values_before_storing_them():
    memory = BitmaskMemory(mask)
    memory.store(address=6, value=11)
    memory.store(address=7, value=101)
    memory.store(address=8, value=0)
    assert memory.sum_values() == 238


def test_bitmask_memory_can_overwrite_values():
    memory = BitmaskMemory(mask)
    memory.store(address=8, value=11)
    memory.store(address=7, value=101)
    memory.store(address=8, value=0)
    assert memory.sum_values() == 165


def test_bitmaks_memory_can_have_mask_updated():
    memory = BitmaskMemory(mask)
    memory.store(address=8, value=11)
    new_mask = Bitmask(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX11111")
    memory.update_mask(new_mask)
    memory.store(address=8, value=11)
    assert memory.sum_values() == 31


def test_set_mask_instruction_updates_memory_mask():
    memory = Mock()
    instruction = SetMaskInstruction(mask.mask)
    instruction.execute(memory)
    memory.update_mask.assert_called_once_with(mask)


def test_write_to_memory_instruction_stores_value():
    memory = Mock()
    instruction = WriteToMemoryInstruction(address=8, value=11)
    instruction.execute(memory)
    memory.store.assert_called_once_with(8, 11)
