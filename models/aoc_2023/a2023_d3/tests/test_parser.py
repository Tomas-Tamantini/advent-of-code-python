from models.common.io import InputFromString
from ..parser import parse_engine_symbols, parse_part_numbers
from ..logic import EngineSymbol, PartNumber


def test_parse_engine_symbols_considers_all_symbols_other_than_dot_and_digits():
    file_content = "..?.+\n.12.*"
    input_reader = InputFromString(file_content)
    symbols = list(parse_engine_symbols(input_reader))
    assert symbols == [
        EngineSymbol(symbol_chr="?", row=0, column=2),
        EngineSymbol(symbol_chr="+", row=0, column=4),
        EngineSymbol(symbol_chr="*", row=1, column=4),
    ]


def test_parse_part_numbers_considers_only_numbers():
    file_content = "467..114..\n...*......\n..03..6333"
    input_reader = InputFromString(file_content)
    numbers = list(parse_part_numbers(input_reader))
    assert numbers == [
        PartNumber(serial="467", row=0, start_column=0),
        PartNumber(serial="114", row=0, start_column=5),
        PartNumber(serial="03", row=2, start_column=2),
        PartNumber(serial="6333", row=2, start_column=6),
    ]
