from collections import defaultdict
from typing import Iterable, Iterator

from models.common.io import InputReader

from .logic import (
    BroadcastModule,
    CommunicationModule,
    ConjunctionModule,
    FlipFlopModule,
    ModuleNetwork,
)


def _parse_communication_module(
    line: str,
) -> tuple[CommunicationModule, tuple[str, ...]]:
    parts = line.split("->")
    module_id = parts[0].strip()
    destinations = tuple(d.strip() for d in parts[1].strip().split(","))
    if module_id[0] == "%":
        module_name = module_id[1:]
        return FlipFlopModule(module_name), destinations
    elif module_id[0] == "&":
        module_name = module_id[1:]
        return ConjunctionModule(module_name, num_inputs=-1), destinations
    else:
        module_name = module_id
        return BroadcastModule(module_name), destinations


def _updated_conjuction_modules(
    conjuction_modules: Iterable[ConjunctionModule], number_of_inputs: dict[str, int]
) -> Iterator[ConjunctionModule]:
    for conjuction_module in conjuction_modules:
        num_inputs = number_of_inputs[conjuction_module.name]
        yield ConjunctionModule(conjuction_module.name, num_inputs)


def parse_module_network(input_reader: InputReader) -> ModuleNetwork:
    connections = dict()
    number_of_inputs = defaultdict(int)
    modules = []
    conjuction_modules = []
    for line in input_reader.read_stripped_lines():
        module, destinations = _parse_communication_module(line)
        connections[module.name] = destinations
        for destination in destinations:
            number_of_inputs[destination] += 1
        if isinstance(module, ConjunctionModule):
            conjuction_modules.append(module)
        else:
            modules.append(module)

    for conjuction_module in _updated_conjuction_modules(
        conjuction_modules, number_of_inputs
    ):
        modules.append(conjuction_module)
    return ModuleNetwork(modules, connections)
