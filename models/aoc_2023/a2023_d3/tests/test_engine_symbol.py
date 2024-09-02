import pytest
from ..logic import PartNumber, EngineSymbol


@pytest.mark.parametrize("row, col", [(2, 0), (0, 2), (-10, -10)])
def test_engine_symbol_is_not_adjacent_to_part_number_not_touching_it(row, col):
    engine_symbol = EngineSymbol(symbol_chr="A", row=0, column=0)
    part_number = PartNumber(serial="123", row=row, start_column=col)
    assert not engine_symbol.is_adjacent_to(part_number)


@pytest.mark.parametrize("row, col", [(20, 7), (21, 7), (21, 11)])
def test_engine_symbol_is_adjacent_to_part_number_touching_it(row, col):
    engine_symbol = EngineSymbol(symbol_chr="A", row=20, column=10)
    part_number = PartNumber(serial="123", row=row, start_column=col)
    assert engine_symbol.is_adjacent_to(part_number)
