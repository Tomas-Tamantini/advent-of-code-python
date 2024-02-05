from typing import Iterator, Protocol
import re
import numpy as np
from datetime import datetime
from collections import defaultdict
from models.graphs import MutableDirectedGraph
from models.vectors import CardinalDirection, Vector2D, TurnDirection
from models.assembly import (
    Instruction,
    CopyInstruction,
    InputInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
)
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
    CityRouter,
    WeightedDirectedGraph,
    Reindeer,
    CookieProperties,
    AuntSue,
    GameOfLifeLights,
    Molecule,
)
from models.aoc_2016 import (
    EncryptedRoom,
    TurtleInstruction,
    ProgrammableScreen,
    ChipFactory,
    ChipAssignment,
    RobotInstruction,
    RobotProgramming,
    FloorConfiguration,
    DiscSystem,
    SpinningDisc,
    StringScrambler,
    MultiStepScrambler,
    LetterSwapScrambler,
    PositionSwapScrambler,
    RotationScrambler,
    LetterBasedRotationScrambler,
    ReversionScrambler,
    LetterMoveScrambler,
    StorageNode,
    AssembunnyProgram,
    IncrementInstruction,
    DecrementInstruction,
    ToggleInstruction,
)
from models.aoc_2017 import (
    TreeBuilder,
    TreeNode,
    ComparisonOperator,
    ConditionalIncrementInstruction,
    ProgramGraph,
    FirewallLayer,
    LayeredFirewall,
    StringTransform,
    Spin,
    Exchange,
    Partner,
    MultiplyInstruction,
    RemainderInstruction,
    RecoverLastFrequencyInstruction,
    Particle,
    ArtBlock,
    SpyMultiplyInstruction,
    BridgeComponent,
    TuringState,
    TuringRule,
)
from models.aoc_2018 import (
    FabricRectangle,
    Guard,
    GuardNap,
    MovingParticle,
    PlantAutomaton,
    InstructionSample,
    ThreeValueInstruction,
    AcreType,
    AddRegisters,
    AddImmediate,
    MultiplyRegisters,
    MultiplyImmediate,
    BitwiseAndRegisters,
    BitwiseAndImmediate,
    BitwiseOrRegisters,
    BitwiseOrImmediate,
    AssignmentRegisters,
    AssignmentImmediate,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
)


class FileReaderProtocol(Protocol):
    def read(self, file_name: str) -> str: ...

    def readlines(self, file_name: str) -> Iterator[str]: ...


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

    @staticmethod
    def default() -> "FileParser":
        return FileParser(FileReader())

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

    def parse_adirected_graph(self, file_name: str) -> CityRouter:
        graph = CityRouter()
        for line in self._file_reader.readlines(file_name):
            nodes_str, distance_str = line.split("=")
            nodes = [n.strip() for n in nodes_str.split("to")]
            distance = int(distance_str)
            graph.add_edge(*nodes, distance)
        return graph

    def parse_weighted_directed_graph(self, file_name: str) -> WeightedDirectedGraph:
        graph = WeightedDirectedGraph()
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

    def parse_game_of_life(
        self, file_name
    ) -> tuple[GameOfLifeLights, set[tuple[int, int]]]:
        live_cells = set()
        for y, line in enumerate(self._file_reader.readlines(file_name)):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    live_cells.add((x, y))
        return GameOfLifeLights(x + 1, y + 1), live_cells

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

    def parse_code_row_and_col(self, file_name: str) -> dict[str, int]:
        text = self._file_reader.read(file_name)
        parts = text.replace(",", "").replace(".", "").split(" ")
        return {"row": int(parts[-3]), "col": int(parts[-1])}

    def parse_turtle_instructions(self, file_name):
        instructions = []
        text = self._file_reader.read(file_name)
        for instruction in text.split(","):
            instruction = instruction.strip()
            turn = TurnDirection(instruction[0])
            steps = int(instruction[1:])
            instructions.append(TurtleInstruction(turn, steps))
        return instructions

    @staticmethod
    def parse_cardinal_direction(direction: str) -> CardinalDirection:
        return {
            "U": CardinalDirection.NORTH,
            "R": CardinalDirection.EAST,
            "D": CardinalDirection.SOUTH,
            "L": CardinalDirection.WEST,
        }[direction]

    def parse_triangle_sides(
        self, file_name: str, read_horizontally: bool
    ) -> Iterator[tuple[int, int, int]]:
        if read_horizontally:
            for line in self._file_reader.readlines(file_name):
                yield tuple(map(int, line.strip().split()))
        else:
            lines = list(self._file_reader.readlines(file_name))
            for i in range(0, len(lines), 3):
                for j in range(3):
                    yield tuple(int(lines[i + k].strip().split()[j]) for k in range(3))

    @staticmethod
    def parse_encrypted_room(room: str) -> EncryptedRoom:
        parts = room.split("[")
        checksum = parts[-1].replace("]", "")
        room_specs = parts[0].split("-")
        sector_id = int(room_specs[-1])
        room_name = "-".join(room_specs[:-1])
        return EncryptedRoom(room_name, sector_id, checksum)

    def parse_programmable_screen_instructions(
        self, file_name: str, screen: ProgrammableScreen
    ) -> None:
        for line in self._file_reader.readlines(file_name):
            if "rect" in line:
                width, height = map(int, line.split("rect")[-1].strip().split("x"))
                screen.rect(width, height)
            elif "rotate row" in line:
                row, offset = map(
                    int, line.replace("y=", "").split("row")[-1].strip().split(" by ")
                )
                screen.rotate_row(row, offset)
            elif "rotate column" in line:
                column, offset = map(
                    int,
                    line.replace("x=", "").split("column")[-1].strip().split(" by "),
                )
                screen.rotate_column(column, offset)

    def _parse_input_assignment(self, line: str) -> ChipAssignment:
        parts = line.strip().split(" ")
        return ChipAssignment(
            chip_id=int(parts[1]),
            instruction=RobotInstruction(destination_id=int(parts[-1])),
        )

    def _parse_robot_program(self, line: str) -> tuple[int, RobotProgramming]:
        parts = line.strip().split(" ")
        robot_id = int(parts[1])
        destination_low = int(parts[-6])
        destination_high = int(parts[-1])
        low_is_output_bin = "output" in parts[5]
        high_is_output_bin = "output" in parts[-2]
        return robot_id, RobotProgramming(
            instruction_low_id_chip=RobotInstruction(
                destination_id=destination_low,
                goes_to_output_bin=low_is_output_bin,
            ),
            instruction_high_id_chip=RobotInstruction(
                destination_id=destination_high,
                goes_to_output_bin=high_is_output_bin,
            ),
        )

    def parse_chip_factory(self, file_name: str) -> ChipFactory:
        input_assignments = list()
        robot_programs = dict()
        for line in self._file_reader.readlines(file_name):
            if "value" in line:
                input_assignments.append(self._parse_input_assignment(line))
            else:
                robot_id, robot_program = self._parse_robot_program(line)
                if robot_id in robot_programs:
                    raise ValueError(f"Robot {robot_id} already has a program")
                robot_programs[robot_id] = robot_program
        return ChipFactory(input_assignments, robot_programs)

    def _parse_floor_configuration(self, line: str) -> FloorConfiguration:
        parts = line.strip().split(" ")
        microchips = []
        generators = []
        for i, part in enumerate(parts):
            if "generator" in part:
                generators.append(parts[i - 1].strip())
            elif "microchip" in part:
                microchips.append(parts[i - 1].replace("-compatible", "").strip())
        return FloorConfiguration(tuple(microchips), tuple(generators))

    def parse_radioisotope_testing_facility_floor_configurations(
        self, file_name: str
    ) -> Iterator[FloorConfiguration]:
        for line in self._file_reader.readlines(file_name):
            yield self._parse_floor_configuration(line)

    def _parse_spinning_disc(self, line: str) -> SpinningDisc:
        parts = line.strip().split(" ")
        num_positions = int(parts[3])
        position_at_time_zero = int(parts[-1].replace(".", ""))
        return SpinningDisc(num_positions, position_at_time_zero)

    def parse_disc_system(self, file_name: str) -> DiscSystem:
        discs = [
            self._parse_spinning_disc(line)
            for line in self._file_reader.readlines(file_name)
        ]
        return DiscSystem(discs)

    def _parse_string_scrambler_function(self, line: str) -> StringScrambler:
        parts = line.strip().split(" ")
        if "swap position" in line:
            return PositionSwapScrambler(
                position_a=int(parts[2]), position_b=int(parts[-1])
            )
        elif "swap letter" in line:
            return LetterSwapScrambler(letter_a=parts[2], letter_b=parts[-1])
        elif "rotate left" in line:
            steps = -int(parts[2])
            return RotationScrambler(steps=steps)
        elif "rotate right" in line:
            steps = int(parts[2])
            return RotationScrambler(steps=steps)
        elif "rotate based on position of letter" in line:
            return LetterBasedRotationScrambler(letter=parts[-1])
        elif "reverse positions" in line:
            return ReversionScrambler(start=int(parts[2]), end=int(parts[-1]))
        elif "move position" in line:
            origin = int(parts[2])
            destination = int(parts[-1])
            return LetterMoveScrambler(origin=origin, destination=destination)
        else:
            raise ValueError(f"Unknown instruction: {line.strip()}")

    def parse_string_scrambler(self, file_name: str) -> MultiStepScrambler:
        scramblers = [
            self._parse_string_scrambler_function(line)
            for line in self._file_reader.readlines(file_name)
        ]
        return MultiStepScrambler(scramblers)

    def _parse_storage_node(self, line: str) -> StorageNode:
        parts = line.strip().split()
        return StorageNode(
            id=parts[0].replace("/dev/grid/node-", ""),
            size=int(parts[1].replace("T", "")),
            used=int(parts[2].replace("T", "")),
        )

    def parse_storage_nodes(self, file_name: str) -> Iterator[StorageNode]:
        for line in self._file_reader.readlines(file_name):
            if "node" in line:
                yield self._parse_storage_node(line)

    def _parse_assembunny_instruction(self, line: str):
        raw_parts = line.strip().split(" ")
        parts = []
        for part in raw_parts[1:]:
            try:
                parts.append(int(part))
            except ValueError:
                parts.append(part)
        if "cpy" in line:
            return CopyInstruction(source=parts[0], destination=parts[1])
        elif "inc" in line:
            return IncrementInstruction(register=parts[0])
        elif "dec" in line:
            return DecrementInstruction(register=parts[0])
        elif "jnz" in line:
            return JumpNotZeroInstruction(
                value_to_compare=parts[0],
                offset=parts[1],
            )
        elif "tgl" in line:
            return ToggleInstruction(offset=parts[0])
        elif "out" in line:
            return OutInstruction(source=parts[0])
        else:
            raise ValueError(f"Unknown instruction: {line.strip()}")

    def parse_assembunny_code(self, file_name) -> AssembunnyProgram:
        instructions = [
            self._parse_assembunny_instruction(line)
            for line in self._file_reader.readlines(file_name)
        ]
        return AssembunnyProgram(instructions)

    def parse_program_tree(self, file_name) -> TreeNode:
        tree_builder = TreeBuilder()
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(" ")
            node_name = parts[0]
            node_weight = int(parts[1].replace("(", "").replace(")", ""))
            children = [p.replace(",", "") for p in parts[3:]]
            tree_builder.add_node(node_name, node_weight, children)
        return tree_builder.root()

    @staticmethod
    def _parse_conditional_increment_instruction(
        line: str,
    ) -> ConditionalIncrementInstruction:
        parts = line.strip().split(" ")
        increment_amount = int(parts[2])
        if "dec" in parts[1]:
            increment_amount = -increment_amount
        return ConditionalIncrementInstruction(
            register_to_increment=parts[0],
            increment_amount=increment_amount,
            comparison_register=parts[4],
            value_to_compare=int(parts[6]),
            comparison_operator=ComparisonOperator(parts[5]),
        )

    def parse_conditional_increment_instructions(
        self, file_name
    ) -> Iterator[ConditionalIncrementInstruction]:
        for line in self._file_reader.readlines(file_name):
            yield self._parse_conditional_increment_instruction(line)

    def parse_program_graph(self, file_name) -> ProgramGraph:
        graph = ProgramGraph()
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(" ")
            node = int(parts[0])
            for neighbor in parts[2:]:
                graph.add_edge(node, int(neighbor.replace(",", "")))
        return graph

    def parse_layered_firewall(self, file_name) -> LayeredFirewall:
        layers = {}
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(":")
            layer_depth = int(parts[0])
            scanning_range = int(parts[1])
            layers[layer_depth] = FirewallLayer(scanning_range=scanning_range)
        return LayeredFirewall(layers)

    def _parse_string_transformer(self, instruction: str) -> StringTransform:
        if instruction.startswith("s"):
            return Spin(int(instruction[1:]))
        elif instruction.startswith("x"):
            parts = instruction[1:].split("/")
            return Exchange(int(parts[0]), int(parts[1]))
        elif instruction.startswith("p"):
            parts = instruction[1:].split("/")
            return Partner(parts[0], parts[1])

    def parse_string_transformers(self, file_name) -> Iterator[StringTransform]:
        for instruction in self._file_reader.read(file_name).split(","):
            yield self._parse_string_transformer(instruction.strip())

    def _parse_duet_instruction(
        self, instruction_str: str, parse_rcv_as_input: bool, spy_multiply: bool
    ) -> Instruction:
        raw_parts = instruction_str.split(" ")
        parts = []
        for part in raw_parts[1:]:
            try:
                parts.append(int(part))
            except ValueError:
                parts.append(part)
        if "snd" in instruction_str:
            return OutInstruction(source=parts[0])
        elif "set" in instruction_str:
            return CopyInstruction(source=parts[1], destination=parts[0])
        elif "add" in instruction_str:
            return AddInstruction(source=parts[1], destination=parts[0])
        elif "sub" in instruction_str:
            return SubtractInstruction(source=parts[1], destination=parts[0])
        elif "mul" in instruction_str:
            return (
                SpyMultiplyInstruction(source=parts[1], destination=parts[0])
                if spy_multiply
                else MultiplyInstruction(source=parts[1], destination=parts[0])
            )
        elif "mod" in instruction_str:
            return RemainderInstruction(source=parts[1], destination=parts[0])
        elif "rcv" in instruction_str:
            return (
                InputInstruction(destination=parts[0])
                if parse_rcv_as_input
                else RecoverLastFrequencyInstruction(source=parts[0])
            )
        elif "jgz" in instruction_str:
            return JumpGreaterThanZeroInstruction(
                value_to_compare=parts[0],
                offset=parts[1],
            )
        elif "jnz" in instruction_str:
            return JumpNotZeroInstruction(
                value_to_compare=parts[0],
                offset=parts[1],
            )
        else:
            raise ValueError(f"Unknown instruction: {instruction_str}")

    def parse_duet_code(
        self,
        file_name,
        parse_rcv_as_input: bool = False,
        spy_multiply: bool = False,
    ) -> Iterator[Instruction]:
        for line in self._file_reader.readlines(file_name):
            yield self._parse_duet_instruction(
                line.strip(), parse_rcv_as_input, spy_multiply
            )

    def parse_particles(self, file_name) -> Iterator[Particle]:
        for particle_id, line in enumerate(self._file_reader.readlines(file_name)):
            parts = line.strip().split(">,")
            position = tuple(map(int, parts[0].replace("p=<", "").split(",")))
            velocity = tuple(map(int, parts[1].replace("v=<", "").split(",")))
            acceleration = tuple(
                map(int, parts[2].replace("a=<", "").replace(">", "").split(","))
            )
            yield Particle(particle_id, position, velocity, acceleration)

    @staticmethod
    def parse_art_block(block: str) -> ArtBlock:
        return ArtBlock(
            np.array(
                [
                    [1 if c == "#" else 0 for c in line.strip()]
                    for line in block.split("/")
                ]
            )
        )

    def parse_art_block_rules(self, file_name: str) -> dict[ArtBlock, ArtBlock]:
        rules = {}
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(" => ")
            rules[self.parse_art_block(parts[0])] = self.parse_art_block(parts[1])
        return rules

    def parse_grid_cluster(self, file_name: str) -> tuple[set[Vector2D], Vector2D]:
        lines = list(self._file_reader.readlines(file_name))
        width = len(lines[0].strip())
        height = len(lines)
        central_position = Vector2D(width // 2, height // 2)
        cluster = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    cluster.add(Vector2D(x, y))
        return cluster, central_position

    def parse_bridge_components(self, file_name: str) -> Iterator[BridgeComponent]:
        for line in self._file_reader.readlines(file_name):
            yield BridgeComponent(*map(int, line.strip().split("/")))

    def parse_turing_machine_specs(
        self, file_name
    ) -> tuple[str, int, dict[TuringState, TuringRule]]:
        lines = list(self._file_reader.readlines(file_name))
        initial_state = lines[0].strip().split()[-1].replace(".", "")
        steps = int(lines[1].strip().split()[-2])
        transition_rules = {}
        for i in range(3, len(lines), 10):
            state_id = lines[i].strip().split()[-1].replace(":", "")
            current_value = int(lines[i + 1].strip().split()[-1].replace(":", ""))
            write_value = int(lines[i + 2].strip().split()[-1].replace(".", ""))
            move = 1 if "right" in lines[i + 3] else -1
            next_state_id = lines[i + 4].strip().split()[-1].replace(".", "")
            transition_rules[TuringState(state_id, current_value)] = TuringRule(
                next_state_id, write_value, move
            )
            current_value = int(lines[i + 5].strip().split()[-1].replace(":", ""))
            write_value = int(lines[i + 6].strip().split()[-1].replace(".", ""))
            move = 1 if "right" in lines[i + 7] else -1
            next_state_id = lines[i + 8].strip().split()[-1].replace(".", "")
            transition_rules[TuringState(state_id, current_value)] = TuringRule(
                next_state_id, write_value, move
            )
        return initial_state, steps, transition_rules

    @staticmethod
    def _parse_fabric_rectangle(line: str) -> FabricRectangle:
        parts = line.strip().split(" ")
        rect_id = int(parts[0].replace("#", ""))
        inches_from_left, inches_from_top = map(
            int, parts[2].replace(":", "").split(",")
        )
        width, height = map(int, parts[3].split("x"))
        return FabricRectangle(
            rect_id, inches_from_left, inches_from_top, width, height
        )

    def parse_fabric_rectangles(self, file_name: str) -> Iterator[FabricRectangle]:
        for line in self._file_reader.readlines(file_name):
            yield self._parse_fabric_rectangle(line)

    def parse_guard_logs(self, file_name: str) -> Iterator[Guard]:
        lines = [l.strip() for l in self._file_reader.readlines(file_name)]
        sorted_lines = sorted(lines, key=lambda l: l[:18])
        guard_logs = defaultdict(list)
        guard_id = -1
        for line in sorted_lines:
            if not line:
                continue
            if "Guard" in line:
                guard_id = int(line.split()[-3].replace("#", ""))
            else:
                event_time = datetime.strptime(
                    line.split("]")[0] + "]", "[%Y-%m-%d %H:%M]"
                )
                guard_logs[guard_id].append(event_time)
        for guard_id, nap_records in guard_logs.items():
            naps = []
            for i in range(0, len(nap_records), 2):
                start = nap_records[i]
                end = nap_records[i + 1]
                naps.append(GuardNap(start, end))
            yield Guard(guard_id, naps)

    def parse_directed_graph(self, file_name: str) -> MutableDirectedGraph:
        graph = MutableDirectedGraph()
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(" ")
            graph.add_edge(parts[1], parts[-3])
        return graph

    def parse_moving_particles(self, file_name) -> Iterator[MovingParticle]:
        for line in self._file_reader.readlines(file_name):
            stripped_line = (
                line.strip()
                .replace(">", "")
                .replace("position=<", "")
                .replace("velocity=<", ",")
            )
            coords = list(map(int, stripped_line.split(",")))
            position = Vector2D(*coords[:2])
            velocity = Vector2D(*coords[2:])
            yield MovingParticle(position, velocity)

    def parse_plant_automaton(self, file_name) -> PlantAutomaton:
        initial_state = set()
        rules = dict()
        for line in self._file_reader.readlines(file_name):
            if "initial state" in line:
                state_str = line.strip().split(":")[-1].strip()
                initial_state = {i for i, c in enumerate(state_str) if c == "#"}
            elif "=> #" in line:
                parts = line.strip().split(" => ")
                configuration = tuple(1 if c == "#" else 0 for c in parts[0])
                rules[configuration] = 1
        return PlantAutomaton(rules, initial_state)

    def parse_instruction_samples(self, file_name) -> Iterator[InstructionSample]:
        lines = list(self._file_reader.readlines(file_name))
        for line_idx, line in enumerate(lines):
            if "Before" in line:
                lb = line.replace("[", "").replace("]", "").strip()
                lv = lines[line_idx + 1].strip()
                la = lines[line_idx + 2].replace("[", "").replace("]", "").strip()

                instruction_values = list(map(int, lv.split()))
                registers_before = tuple(map(int, lb.split(":")[1].split(",")))
                registers_after = tuple(map(int, la.split(":")[1].split(",")))

                yield InstructionSample(
                    op_code=instruction_values[0],
                    instruction_values=tuple(instruction_values[1:]),
                    registers_before=registers_before,
                    registers_after=registers_after,
                )

    def parse_unknown_op_code_program(
        self,
        file_name,
        op_code_to_instruction: dict[int, type[ThreeValueInstruction]],
    ) -> Iterator[ThreeValueInstruction]:
        instructions = []
        for line in reversed(list(self._file_reader.readlines(file_name))):
            if "After:" in line:
                break
            if not line.strip():
                continue
            values = list(map(int, line.strip().split()))
            op_code = values[0]
            instruction_type = op_code_to_instruction[op_code]
            instructions.append(instruction_type(*values[1:]))
        yield from reversed(instructions)

    def parse_position_ranges(self, file_name: str) -> Iterator[Vector2D]:
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(",")
            coords = dict()
            for part in parts:
                key, value = part.split("=")
                min_coord = int(value.split("..")[0])
                max_coord = int(value.split("..")[-1])
                coords[key.strip()] = (min_coord, max_coord)
            for x in range(coords["x"][0], coords["x"][1] + 1):
                for y in range(coords["y"][0], coords["y"][1] + 1):
                    yield Vector2D(x, y)

    def parse_lumber_area(self, file_name: str) -> dict[Vector2D, AcreType]:
        cells = {}
        for y, line in enumerate(self._file_reader.readlines(file_name)):
            for x, char in enumerate(line.strip()):
                acre_type = AcreType(char)
                if acre_type != AcreType.OPEN:
                    cells[Vector2D(x, y)] = acre_type

        return cells

    def parse_three_value_instructions(
        self, file_name: str
    ) -> Iterator[ThreeValueInstruction]:
        register_bound_to_pc = None
        instruction_types = {
            "addr": AddRegisters,
            "addi": AddImmediate,
            "mulr": MultiplyRegisters,
            "muli": MultiplyImmediate,
            "banr": BitwiseAndRegisters,
            "bani": BitwiseAndImmediate,
            "borr": BitwiseOrRegisters,
            "bori": BitwiseOrImmediate,
            "setr": AssignmentRegisters,
            "seti": AssignmentImmediate,
            "gtir": GreaterThanImmediateRegister,
            "gtri": GreaterThanRegisterImmediate,
            "gtrr": GreaterThanRegisterRegister,
            "eqir": EqualImmediateRegister,
            "eqri": EqualRegisterImmediate,
            "eqrr": EqualRegisterRegister,
        }
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split()
            if "#ip" in parts:
                register_bound_to_pc = int(parts[-1])
            else:
                instruction_type = instruction_types[parts[0]]
                yield instruction_type(*map(int, parts[1:]), register_bound_to_pc)
