from models.aoc_2015 import (
    XmasPresent,
    LightGrid,
    LightGridRegion,
    LogicGatesCircuit,
    DoNothingGate,
    AndGate,
    OrGate,
    LeftShiftGate,
    RightShiftGate,
    NotGate,
    AdirectedGraph,
    DirectedGraph,
    Reindeer,
)
from typing import Iterator


def parse_xmas_presents(file_name: str) -> Iterator[XmasPresent]:
    with open(file_name, "r") as f:
        for line in f:
            yield XmasPresent(*map(int, line.split("x")))


def parse_and_give_light_grid_instruction(
    instruction: str, grid: LightGrid, use_elvish_tongue: bool = False
) -> None:
    parts = instruction.strip().split(" ")
    region = LightGridRegion(
        tuple(map(int, parts[-3].split(","))),
        tuple(map(int, parts[-1].split(","))),
    )
    if "on" in instruction:
        if use_elvish_tongue:
            grid.increase_brightness(region, increase=1)
        else:
            grid.turn_on(region)
    elif "off" in instruction:
        if use_elvish_tongue:
            grid.decrease_brightness(region, decrease=1)
        else:
            grid.turn_off(region)
    else:
        if use_elvish_tongue:
            grid.increase_brightness(region, increase=2)
        else:
            grid.toggle(region)


def _parse_logic_gate_input(gate, input: str) -> None:
    try:
        input_signal = int(input)
        gate.add_input_signal(input_signal)
    except:
        gate.add_input_wire(input.strip())


def parse_logic_gates_circuit(circuit_spec: str) -> LogicGatesCircuit:
    # TODO: Read directly from file
    circuit = LogicGatesCircuit()
    for line in circuit_spec.split("\n"):
        if "->" not in line:
            continue
        input_str, output_str = line.split("->")
        output_wire = output_str.strip()
        if "AND" in input_str:
            gate = AndGate()
            inputs = input_str.split("AND")
        elif "OR" in input_str:
            gate = OrGate()
            inputs = input_str.split("OR")
        elif "LSHIFT" in input_str:
            input_wire_str, shift_str = input_str.split("LSHIFT")
            gate = LeftShiftGate(shift=int(shift_str), num_bits=16)
            inputs = [input_wire_str]
        elif "RSHIFT" in input_str:
            input_wire_str, shift_str = input_str.split("RSHIFT")
            gate = RightShiftGate(shift=int(shift_str), num_bits=16)
            inputs = [input_wire_str]
        elif "NOT" in input_str:
            gate = NotGate(num_bits=16)
            _, input_wire_str = input_str.split("NOT")
            inputs = [input_wire_str]
        else:
            gate = DoNothingGate()
            _parse_logic_gate_input(gate, input_str)
            inputs = [input_str]
        for input in inputs:
            _parse_logic_gate_input(gate, input)
        circuit.add_gate(gate, output_wire)
    return circuit


def parse_adirected_graph(adjacencies: str) -> AdirectedGraph:
    graph = AdirectedGraph()
    for line in adjacencies.split("\n"):
        nodes_str, distance_str = line.split("=")
        nodes = [n.strip() for n in nodes_str.split("to")]
        distance = int(distance_str)
        graph.add_edge(*nodes, distance)
    return graph


def parse_directed_graph(adjacencies: str) -> DirectedGraph:
    graph = DirectedGraph()
    for line in adjacencies.split("\n"):
        sentence_parts = line.strip().split(" ")
        node_a = sentence_parts[0].strip()
        node_b = sentence_parts[-1].replace(".", "").strip()
        cost = int(sentence_parts[3])
        if "lose" in line:
            cost = -cost
        graph.add_edge(node_a, node_b, cost)
    return graph


def parse_reindeer(reindeer_str: str) -> Reindeer:
    sentence_parts = reindeer_str.split(" ")
    return Reindeer(
        flight_speed=int(sentence_parts[3]),
        flight_interval=int(sentence_parts[6]),
        rest_interval=int(sentence_parts[13]),
    )
