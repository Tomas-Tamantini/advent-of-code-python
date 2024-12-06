from dataclasses import dataclass
from typing import Callable, Iterator, Optional, Union

from models.common.io import InputReader
from models.common.polynomials import Polynomial, RationalFunction

from .operation_monkeys import BinaryOperationMonkey, LeafMonkey, OperationMonkey


@dataclass(frozen=True)
class _UnparsedMonkey:
    name: str
    children_names: tuple[str, str]
    operation_symbol: chr


def _parse_operation(
    operation_symbol: chr,
) -> Callable[[RationalFunction, RationalFunction], RationalFunction]:
    return {
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
        "-": lambda x, y: x - y,
        "/": lambda x, y: x / y,
    }[operation_symbol]


def _parse_children(
    unparsed_monkey: _UnparsedMonkey,
    parsed_monkeys: dict[str, OperationMonkey],
    unparsed_monkeys: dict[str, _UnparsedMonkey],
) -> Iterator[OperationMonkey]:
    for child_name in unparsed_monkey.children_names:
        child = parsed_monkeys.get(child_name)
        if child is None:
            child = _parse_binary_operation_monkey(
                child_name, parsed_monkeys, unparsed_monkeys
            )
        yield child


def _parse_binary_operation_monkey(
    monkey_name: str,
    parsed_monkeys: dict[str, OperationMonkey],
    unparsed_monkeys: dict[str, _UnparsedMonkey],
) -> BinaryOperationMonkey:
    unparsed_monkey = unparsed_monkeys.pop(monkey_name)
    children = _parse_children(unparsed_monkey, parsed_monkeys, unparsed_monkeys)
    operation = _parse_operation(unparsed_monkey.operation_symbol)
    parsed_monkey = BinaryOperationMonkey(monkey_name, *children, operation)
    parsed_monkeys[monkey_name] = parsed_monkey
    return parsed_monkey


def _parse_binary_operation_monkeys(
    parsed_monkeys: dict[str, OperationMonkey],
    unparsed_monkeys: dict[str, _UnparsedMonkey],
) -> None:
    while unparsed_monkeys:
        monkey_name = next(iter(unparsed_monkeys))
        _parse_binary_operation_monkey(monkey_name, parsed_monkeys, unparsed_monkeys)


def _initial_parsing(
    line: str, monkey_with_unknown_value: Optional[str]
) -> Union[LeafMonkey, _UnparsedMonkey]:
    parts = line.split(":")
    monkey_name = parts[0].strip()
    if monkey_name == monkey_with_unknown_value:
        return LeafMonkey(
            name=monkey_name,
            rational_function=RationalFunction(
                numerator=Polynomial((0, 1)), denominator=Polynomial((1,))
            ),
        )
    try:
        value = int(parts[1].strip())
        rational_function = RationalFunction(
            numerator=Polynomial((value,)), denominator=Polynomial((1,))
        )
        return LeafMonkey(monkey_name, rational_function)
    except ValueError:
        left_name, operation_symbol, right_name = parts[1].strip().split()
        return _UnparsedMonkey(
            name=monkey_name,
            children_names=(left_name, right_name),
            operation_symbol=operation_symbol,
        )


def parse_operation_monkeys(
    input_reader: InputReader, monkey_with_unknown_value: Optional[str] = None
) -> list[OperationMonkey]:
    unparsed_monkeys = dict()
    parsed_monkeys = dict()
    for line in input_reader.read_stripped_lines():
        monkey = _initial_parsing(line, monkey_with_unknown_value)
        if isinstance(monkey, LeafMonkey):
            parsed_monkeys[monkey.name] = monkey
        else:
            unparsed_monkeys[monkey.name] = monkey
    _parse_binary_operation_monkeys(parsed_monkeys, unparsed_monkeys)

    return list(parsed_monkeys.values())
