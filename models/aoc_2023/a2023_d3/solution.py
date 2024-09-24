from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_engine_symbols, parse_part_numbers
from .logic import EngineSymbol, PartNumber
from math import prod


def aoc_2023_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 3, "Gear Ratios")
    io_handler.output_writer.write_header(problem_id)
    adjacencies = _get_adjacencies(io_handler)

    part_numbers = {
        part_number for adjacent in adjacencies.values() for part_number in adjacent
    }
    sum_part_numbers = sum(part.number for part in part_numbers)
    yield ProblemSolution(
        problem_id,
        f"The sum of part numbers is {sum_part_numbers}",
        result=sum_part_numbers,
        part=1,
    )

    sum_gear_ratios = 0
    for symbol, adjacent_parts in adjacencies.items():
        if _is_gear(symbol, adjacent_parts):
            sum_gear_ratios += prod(part.number for part in adjacent_parts)

    yield ProblemSolution(
        problem_id,
        f"The sum of gear ratios is {sum_gear_ratios}",
        result=sum_gear_ratios,
        part=2,
    )


def _get_adjacencies(io_handler: IOHandler) -> dict[EngineSymbol, set[PartNumber]]:
    engine_symbols = set(parse_engine_symbols(io_handler.input_reader))
    part_numbers = set(parse_part_numbers(io_handler.input_reader))
    return {
        symbol: {part for part in part_numbers if symbol.is_adjacent_to(part)}
        for symbol in engine_symbols
    }


def _is_gear(symbol: EngineSymbol, adjacent_part_numbers: set[PartNumber]) -> bool:
    return symbol.symbol_chr == "*" and len(adjacent_part_numbers) == 2
