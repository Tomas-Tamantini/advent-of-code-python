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
    CookieProperties,
    Fighter,
    AuntSue,
    GameOfLife,
    Molecule,
)
from typing import Iterator, Protocol
import re


class FileReaderProtocol(Protocol):
    def read(self, file_name: str) -> str:
        ...

    def readlines(self, file_name: str) -> Iterator[str]:
        ...


class FileReader:
    def read(self, file_name: str) -> str:
        with open(file_name, "r") as f:
            return f.read()

    def readlines(self, file_name: str) -> Iterator[str]:
        with open(file_name, "r") as f:
            yield from f.readlines()


class FileParser:
    def __init__(self, file_reader: FileReaderProtocol) -> None:
        self._file_reader = file_reader

    def parse_xmas_presents(self, file_name: str) -> Iterator[XmasPresent]:
        for l in self._file_reader.readlines(file_name):
            yield XmasPresent(*map(int, l.split("x")))

    @staticmethod
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

    @staticmethod
    def _parse_logic_gate_input(gate, input: str) -> None:
        try:
            input_signal = int(input)
            gate.add_input_signal(input_signal)
        except:
            gate.add_input_wire(input.strip())

    def parse_logic_gates_circuit(self, file_name: str) -> LogicGatesCircuit:
        circuit = LogicGatesCircuit()
        for line in self._file_reader.readlines(file_name):
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
                self._parse_logic_gate_input(gate, input_str)
                inputs = [input_str]
            for input in inputs:
                self._parse_logic_gate_input(gate, input)
            circuit.add_gate(gate, output_wire)
        return circuit

    def parse_adirected_graph(self, file_name: str) -> AdirectedGraph:
        graph = AdirectedGraph()
        for line in self._file_reader.readlines(file_name):
            nodes_str, distance_str = line.split("=")
            nodes = [n.strip() for n in nodes_str.split("to")]
            distance = int(distance_str)
            graph.add_edge(*nodes, distance)
        return graph

    def parse_directed_graph(self, file_name: str) -> DirectedGraph:
        graph = DirectedGraph()
        for line in self._file_reader.readlines(file_name):
            sentence_parts = line.strip().split(" ")
            node_a = sentence_parts[0].strip()
            node_b = sentence_parts[-1].replace(".", "").strip()
            cost = int(sentence_parts[3])
            if "lose" in line:
                cost = -cost
            graph.add_edge(node_a, node_b, cost)
        return graph

    @staticmethod
    def parse_reindeer(reindeer_str: str) -> Reindeer:
        sentence_parts = reindeer_str.split(" ")
        return Reindeer(
            flight_speed=int(sentence_parts[3]),
            flight_interval=int(sentence_parts[6]),
            rest_interval=int(sentence_parts[13]),
        )

    @staticmethod
    def parse_cookie_properties(properties_str: str) -> CookieProperties:
        parts = properties_str.replace(",", "").split(" ")
        return CookieProperties(
            capacity=int(parts[2]),
            durability=int(parts[4]),
            flavor=int(parts[6]),
            texture=int(parts[8]),
            calories=int(parts[10]),
        )

    def parse_rpg_boss(self, file_name: str) -> dict[str, int]:
        attributes = {}
        for line in self._file_reader.readlines(file_name):
            parts = line.split(":")
            value = int(parts[-1])
            if "Hit Points" in line:
                attributes["hit_points"] = value
            elif "Damage" in line:
                attributes["damage"] = value
            elif "Armor" in line:
                attributes["armor"] = value
        return attributes

    def parse_aunt_sue_collection(self, file_name) -> Iterator[AuntSue]:
        for line in self._file_reader.readlines(file_name):
            parts = line.split(":", 1)
            sue_id = int(parts[0].replace("Sue ", ""))
            attributes = {}
            for attribute in parts[1].split(","):
                key, value = attribute.split(":")
                attributes[key.strip()] = int(value.strip())
            yield AuntSue(sue_id, attributes)

    def parse_game_of_life(self, file_name) -> tuple[GameOfLife, set[tuple[int, int]]]:
        live_cells = set()
        for y, line in enumerate(self._file_reader.readlines(file_name)):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    live_cells.add((x, y))
        return GameOfLife(x + 1, y + 1), live_cells

    @staticmethod
    def _parse_molecule(molecule_str: str) -> Molecule:
        atom_pattern = re.compile(r"([A-Z][a-z]?)")
        atoms = re.findall(atom_pattern, molecule_str)
        return Molecule(tuple(atoms))

    def parse_molecule_replacements(
        self, file_name: str
    ) -> tuple[Molecule, dict[str, tuple[Molecule]]]:
        lines = list(self._file_reader.readlines(file_name))
        molecule = self._parse_molecule(lines[-1].strip())
        replacements = {}
        for line in lines:
            if "=>" not in line:
                continue
            atom, replace_molecule_str = line.strip().split(" => ")
            if atom not in replacements:
                replacements[atom] = []
            replacements[atom].append(self._parse_molecule(replace_molecule_str))
        return molecule, {k: tuple(v) for k, v in replacements.items()}
