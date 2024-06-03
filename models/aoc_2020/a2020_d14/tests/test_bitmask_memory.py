from unittest.mock import Mock
from ..bitmask_memory import (
    Bitmask,
    FloatingBitmask,
    BitmaskMemory,
    SetMaskInstruction,
    WriteToMemoryInstruction,
)

mask = Bitmask(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")


def test_bitmask_overwrites_bits_in_value():
    assert mask.apply(11) == 73
    assert mask.apply(101) == 101
    assert mask.apply(0) == 64


def test_floating_bitmask_does_not_change_bit_where_mask_is_zero():
    floating_mask = FloatingBitmask(mask="000000000")
    assert list(floating_mask.apply(11)) == [11]


def test_floating_bitmask_overwrites_bits_where_mask_is_one():
    floating_mask = FloatingBitmask(mask="11111111")
    assert list(floating_mask.apply(11)) == [255]


def test_floating_bitmask_yields_all_options_where_mask_is_x():
    floating_mask = FloatingBitmask(mask="X1X0")
    assert list(floating_mask.apply(11)) == [5, 7, 13, 15]


def test_bitmask_memory_starts_empty():
    memory = BitmaskMemory()
    assert memory.sum_values() == 0


def test_bitmask_memory_stores_values_in_memory():
    memory = BitmaskMemory()
    memory.store(address=3, value=123)
    memory.store(address=7, value=321)
    assert memory.sum_values() == 444


def test_bitmask_memory_transforms_values_before_storing_them_if_given_value_mask():
    memory = BitmaskMemory(value_mask=mask)
    memory.store(address=6, value=11)
    memory.store(address=7, value=101)
    memory.store(address=8, value=0)
    assert memory.sum_values() == 238


def test_bitmask_memory_can_overwrite_values():
    memory = BitmaskMemory(value_mask=mask)
    memory.store(address=8, value=11)
    memory.store(address=7, value=101)
    memory.store(address=8, value=0)
    assert memory.sum_values() == 165


def test_bitmaks_memory_can_have_values_mask_updated():
    memory = BitmaskMemory(value_mask=mask)
    memory.store(address=8, value=11)
    new_mask = Bitmask(mask="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX11111")
    memory.update_value_mask(new_mask)
    memory.store(address=8, value=11)
    assert memory.sum_values() == 31


def test_bitmask_memory_transforms_memory_address_before_storing_if_given_address_mask():
    memory = BitmaskMemory(
        address_mask=FloatingBitmask("000000000000000000000000000000X1001X")
    )
    memory.store(address=42, value=100)
    assert memory.sum_values() == 400


def test_bitmaks_memory_can_have_address_mask_updated():
    memory = BitmaskMemory(
        address_mask=FloatingBitmask("000000000000000000000000000000X1001X")
    )
    memory.store(address=42, value=100)
    memory.update_address_mask(FloatingBitmask("00000000000000000000000000000000X0XX"))
    memory.store(address=26, value=1)
    assert memory.sum_values() == 208


def test_set_mask_instruction_updates_values_mask_depending_on_flag():
    memory = Mock()
    instruction = SetMaskInstruction(mask.mask, is_address_mask=False)
    instruction.execute(memory)
    memory.update_value_mask.assert_called_once_with(mask)


def test_set_mask_instruction_updates_address_mask_depending_on_flag():
    memory = Mock()
    instruction = SetMaskInstruction(mask.mask, is_address_mask=True)
    instruction.execute(memory)
    memory.update_address_mask.assert_called_once_with(FloatingBitmask(mask.mask))


def test_write_to_memory_instruction_stores_value():
    memory = Mock()
    instruction = WriteToMemoryInstruction(address=8, value=11)
    instruction.execute(memory)
    memory.store.assert_called_once_with(8, 11)
