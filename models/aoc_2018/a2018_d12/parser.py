from models.common.io import InputReader
from .plant_automaton import PlantAutomaton


def parse_plant_automaton(input_reader: InputReader) -> PlantAutomaton:
    initial_state = set()
    rules = dict()
    for line in input_reader.readlines():
        if "initial state" in line:
            state_str = line.strip().split(":")[-1].strip()
            initial_state = {i for i, c in enumerate(state_str) if c == "#"}
        elif "=> #" in line:
            parts = line.strip().split(" => ")
            configuration = tuple(1 if c == "#" else 0 for c in parts[0])
            rules[configuration] = 1
    return PlantAutomaton(rules, initial_state)
