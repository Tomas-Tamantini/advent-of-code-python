from typing import Iterator, Protocol, Optional, Hashable
from dataclasses import dataclass
import re
import numpy as np
from datetime import datetime
from collections import defaultdict
from models.graphs import DirectedGraph
from models.vectors import (
    CardinalDirection,
    Vector2D,
    TurnDirection,
    Vector3D,
    HexagonalDirection,
)
from models.char_grid import CharacterGrid
from models.assembly import (
    Instruction,
    CopyInstruction,
    InputInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
    ContextFreeGrammar,
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
    SeatingArrangements,
    Reindeer,
    CookieProperties,
    AuntSue,
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
    TeleportNanobot,
    AttackType,
    ArmyGroup,
    InfectionGameState,
)
from models.aoc_2019 import (
    CelestialBody,
    ChemicalQuantity,
    ChemicalReaction,
    TunnelMaze,
    PortalMaze,
    RecursiveDonutMaze,
    DealIntoNewStackShuffle,
    CutCardsShuffle,
    DealWithIncrementShuffle,
    MultiTechniqueShuffle,
)
from models.aoc_2020 import (
    PasswordPolicy,
    RangePasswordPolicy,
    PositionalPasswordPolicy,
    CustomsGroup,
    LuggageRule,
    LuggageRules,
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
    NavigationInstruction,
    MoveShipForwardInstruction,
    MoveShipInstruction,
    TurnShipInstruction,
    MoveTowardsWaypointInstruction,
    MoveWaypointInstruction,
    RotateWaypointInstruction,
    BusSchedule,
    BitmaskInstruction,
    SetMaskInstruction,
    WriteToMemoryInstruction,
    TicketValidator,
    TicketFieldValidator,
    RangeInterval,
    JigsawPieceBinaryImage,
    Food,
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


@dataclass
class _ParsedTicketValidator:
    validator: TicketValidator
    my_ticket: tuple[int]
    nearby_tickets: list[tuple[int]]


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

    def parse_seating_arrangement(self, file_name: str) -> SeatingArrangements:
        graph = SeatingArrangements()
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
            position = Vector3D(*map(int, parts[0].replace("p=<", "").split(",")))
            velocity = Vector3D(*map(int, parts[1].replace("v=<", "").split(",")))
            acceleration = Vector3D(
                *map(int, parts[2].replace("a=<", "").replace(">", "").split(","))
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

    def parse_directed_graph(self, file_name: str) -> DirectedGraph:
        graph = DirectedGraph()
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

    def parse_nanobots(self, file_name: str) -> Iterator[TeleportNanobot]:
        for line in self._file_reader.readlines(file_name):
            numbers = tuple(
                map(
                    int,
                    line.replace("pos=<", "")
                    .replace(">", "")
                    .replace("r=", "")
                    .split(","),
                )
            )
            yield TeleportNanobot(radius=numbers[-1], position=Vector3D(*numbers[:3]))

    def _parse_army_group(self, group_id: int, line: str) -> ArmyGroup:
        line = line.strip()
        units = int(line.split(" ")[0])
        hit_points = int(line.split(" ")[4])
        initiative = int(line.split(" ")[-1])
        attack_damage = int(line.split(" ")[-6])
        attack_type = AttackType.from_str(line.split(" ")[-5])
        weaknesses = []
        immunities = []
        if "(" in line:
            within_parentheses = line.split("(")[-1].split(")")[0]
            for part in within_parentheses.split(";"):
                if "weak" in part:
                    weaknesses = [
                        AttackType.from_str(p.strip())
                        for p in part.replace("weak to", "").split(",")
                    ]
                else:
                    immunities = [
                        AttackType.from_str(p.strip())
                        for p in part.replace("immune to", "").split(",")
                    ]

        return ArmyGroup(
            group_id=group_id,
            num_units=units,
            hit_points_per_unit=hit_points,
            attack_damage_per_unit=attack_damage,
            initiative=initiative,
            attack_type=attack_type,
            weaknesses=tuple(weaknesses),
            immunities=tuple(immunities),
        )

    def parse_infection_game(self, file_name: str) -> InfectionGameState:
        immune_system_armies = []
        infection_armies = []
        loading_immune_system = True
        group_id = 1
        for line in self._file_reader.readlines(file_name):
            if "Infection" in line:
                loading_immune_system = False
            elif "Immune" in line:
                loading_immune_system = True
            elif "units" in line:
                army_group = self._parse_army_group(group_id, line)
                group_id += 1
                if loading_immune_system:
                    immune_system_armies.append(army_group)
                else:
                    infection_armies.append(army_group)
        return InfectionGameState(
            immune_system_armies=tuple(immune_system_armies),
            infection_armies=tuple(infection_armies),
        )

    def parse_directions(
        self, file_name: str
    ) -> Iterator[list[tuple[CardinalDirection, int]]]:
        for line in self._file_reader.readlines(file_name):
            yield [
                (self.parse_cardinal_direction(part.strip()[0]), int(part.strip()[1:]))
                for part in line.strip().split(",")
            ]

    def parse_celestial_bodies(self, file_name: str) -> CelestialBody:
        bodies = dict()
        for line in self._file_reader.readlines(file_name):
            parts = line.strip().split(")")
            parent = parts[0]
            child = parts[1]
            if parent not in bodies:
                bodies[parent] = CelestialBody(parent)
            if child not in bodies:
                bodies[child] = CelestialBody(child)
            bodies[parent].add_satellite(bodies[child])
        return bodies["COM"]

    @staticmethod
    def parse_vector_3d(vector_str: str) -> Vector3D:
        coordinates = (
            vector_str.replace("<", "")
            .replace(">", "")
            .replace("=", "")
            .replace("x", "")
            .replace("y", "")
            .replace("z", "")
            .split(",")
        )
        return Vector3D(*map(int, coordinates))

    @staticmethod
    def _parse_chemical_quantity(quantity_str: str) -> ChemicalQuantity:
        quantity, chemical = quantity_str.split()
        return ChemicalQuantity(chemical=chemical, quantity=int(quantity))

    @staticmethod
    def _parse_chemical_reaction(reaction_str: str) -> ChemicalReaction:
        input_str, output_str = reaction_str.split(" => ")
        output = FileParser._parse_chemical_quantity(output_str)
        inputs = tuple(
            FileParser._parse_chemical_quantity(q) for q in input_str.split(", ")
        )
        return ChemicalReaction(inputs, output)

    def parse_chemical_reactions(self, file_name: str) -> Iterator[ChemicalReaction]:
        for line in self._file_reader.readlines(file_name):
            yield self._parse_chemical_reaction(line.strip())

    @staticmethod
    def _tunnel_updated_characters(
        grid: CharacterGrid, split_entrance_four_ways: bool
    ) -> dict[Vector2D, chr]:
        if not split_entrance_four_ways:
            return dict()
        entrance_position = next(grid.positions_with_value("@"))
        updated_chars = dict()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                offset = Vector2D(dx, dy)
                new_char = "@" if offset.manhattan_size == 2 else "#"
                updated_chars[entrance_position + offset] = new_char
        return updated_chars

    def parse_tunnel_maze(
        self, file_name: str, split_entrance_four_ways: bool = False
    ) -> TunnelMaze:
        content = self._file_reader.read(file_name)
        grid = CharacterGrid(content)
        maze = TunnelMaze()
        updated_chars = self._tunnel_updated_characters(grid, split_entrance_four_ways)
        for position in grid.positions():
            original_char = grid.tiles[position]
            actual_char = updated_chars.get(position, original_char)
            if actual_char == ".":
                maze.add_open_passage(position)
            if actual_char == "@":
                maze.add_entrance(position)
            if actual_char.islower():
                maze.add_key(position, key_id=original_char)
            if actual_char.isupper():
                maze.add_door(position, corresponding_key_id=actual_char.lower())
        return maze

    @staticmethod
    def _portal_id(position: Vector2D, lines: list[str]) -> Optional[str]:
        for direction in CardinalDirection:
            neighbor_position = position.move(direction)
            if neighbor_position.y < 0 or neighbor_position.y >= len(lines):
                continue
            neighbor_line = lines[neighbor_position.y]
            if neighbor_position.x < 0 or neighbor_position.x >= len(neighbor_line):
                continue
            neighbor_char = neighbor_line[neighbor_position.x]
            if not neighbor_char.isupper():
                continue
            other_char_position = neighbor_position.move(direction)
            other_char = lines[other_char_position.y][other_char_position.x]
            return (
                neighbor_char + other_char
                if direction in {CardinalDirection.NORTH, CardinalDirection.EAST}
                else other_char + neighbor_char
            )

    @staticmethod
    def _open_passage_tiles(lines: list[str]) -> Iterator[Vector2D]:
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == ".":
                    yield Vector2D(x, y)

    def parse_portal_maze(self, file_name: str) -> PortalMaze:
        portals = defaultdict(list)
        maze = PortalMaze()
        lines = list(self._file_reader.readlines(file_name))
        for position in self._open_passage_tiles(lines):
            maze.add_node(position)
            portal_id = self._portal_id(position, lines)
            if portal_id == "AA":
                maze.set_entrance(position)
            elif portal_id == "ZZ":
                maze.set_exit(position)
            elif portal_id is not None:
                portals[portal_id].append(position)
        for positions in portals.values():
            maze.add_portal(*positions)

        return maze

    def _is_inner_edge_of_donut_maze(
        self, position: Vector2D, lines: list[str]
    ) -> bool:
        for direction in CardinalDirection:
            intersected_other_tile = False
            new_position = position.move(direction)
            while (0 <= new_position.y < len(lines)) and (
                0 <= new_position.x < len(lines[new_position.y])
            ):
                character = lines[new_position.y][new_position.x]
                if character in {"#", "."}:
                    intersected_other_tile = True
                    break
                new_position = new_position.move(direction)
            if not intersected_other_tile:
                return False
        return True

    def parse_recursive_donut_maze(self, file_name: str) -> RecursiveDonutMaze:
        portals = defaultdict(dict)
        maze = RecursiveDonutMaze()
        lines = list(self._file_reader.readlines(file_name))
        for position in self._open_passage_tiles(lines):
            maze.add_node(position)
            portal_id = self._portal_id(position, lines)
            if portal_id == "AA":
                maze.set_entrance(position)
            elif portal_id == "ZZ":
                maze.set_exit(position)
            elif portal_id is not None:
                kwarg = (
                    "step_up"
                    if self._is_inner_edge_of_donut_maze(position, lines)
                    else "step_down"
                )
                portals[portal_id][kwarg] = position

        for positions in portals.values():
            maze.add_portal(**positions)

        return maze

    def parse_multi_technique_shuffle(self, file_name: str) -> MultiTechniqueShuffle:
        techniques = []
        for line in self._file_reader.readlines(file_name):
            if "deal into new stack" in line:
                techniques.append(DealIntoNewStackShuffle())
            elif "cut" in line:
                techniques.append(CutCardsShuffle(int(line.split()[-1])))
            elif "deal with increment" in line:
                techniques.append(DealWithIncrementShuffle(int(line.split()[-1])))
        return MultiTechniqueShuffle(techniques)

    @staticmethod
    def _parse_password_policy_and_password(
        line: str, use_range_policy: bool
    ) -> tuple[PasswordPolicy, str]:
        parts = line.split(":")
        policy_parts = parts[0].split(" ")
        num_a, num_b = map(int, policy_parts[0].split("-"))
        letter = policy_parts[1]
        password = parts[1].strip()
        if use_range_policy:
            return RangePasswordPolicy(letter, num_a, num_b), password
        else:
            return PositionalPasswordPolicy(letter, num_a, num_b), password

    def parse_password_policies_and_passwords(
        self, file_name: str, use_range_policy: bool
    ) -> Iterator[tuple[PasswordPolicy, str]]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield self._parse_password_policy_and_password(
                    line.strip(), use_range_policy
                )

    def parse_passports(self, file_name: str) -> Iterator[dict[str, str]]:
        passport = {}
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                parts = line.strip().split()
                for part in parts:
                    key, value = part.split(":")
                    passport[key] = value
            else:
                if passport:
                    yield passport
                passport = {}
        if passport:
            yield passport

    def parse_plane_seat_ids(self, file_name: str) -> Iterator[int]:
        for line in self._file_reader.readlines(file_name):
            line = line.strip()
            if line:
                row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
                col = int(line[7:].replace("L", "0").replace("R", "1"), 2)
                yield row * 8 + col

    def parse_form_answers_by_groups(self, file_name: str) -> Iterator[CustomsGroup]:
        current_group = CustomsGroup()
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                current_group.add_individual_answers(set(line.strip()))
            else:
                if current_group.answers:
                    yield current_group
                current_group = CustomsGroup()
        if current_group.answers:
            yield current_group

    def _parse_luggage_rule(self, rule: str) -> LuggageRule:
        parts = rule.split("contain")
        container_bag = parts[0].strip().replace("bags", "").replace("bag", "").strip()

        contained_bags = dict()
        for part in parts[1].split(","):
            part = (
                part.strip()
                .replace("bags", "")
                .replace("bag", "")
                .replace(".", "")
                .strip()
            )
            if "no other" in part:
                continue
            quantity, bag = part.split(" ", 1)
            contained_bags[bag] = int(quantity)

        return LuggageRule(bag=container_bag, contains=contained_bags)

    def parse_luggage_rules(self, file_name: str) -> LuggageRules:
        rules = LuggageRules()
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                rules.add_rule(self._parse_luggage_rule(line.strip()))
        return rules

    def _parse_game_console_instruction(self, instruction: str) -> Instruction:
        parts = instruction.split()
        operation = parts[0].strip()
        value = int(parts[1])
        if operation == "nop":
            return JumpOrNoOpInstruction(offset=value, is_jump=False)
        elif operation == "acc":
            return IncrementGlobalAccumulatorInstruction(increment=value)
        elif operation == "jmp":
            return JumpOrNoOpInstruction(offset=value, is_jump=True)
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def parse_game_console_instructions(self, file_name: str) -> Iterator[Instruction]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield self._parse_game_console_instruction(line.strip())

    def _parse_navigation_instruction(
        self, instruction: str, relative_to_waypoint: bool
    ) -> NavigationInstruction:
        action = instruction[0]
        value = int(instruction[1:])
        directions = {
            "N": CardinalDirection.NORTH,
            "S": CardinalDirection.SOUTH,
            "E": CardinalDirection.EAST,
            "W": CardinalDirection.WEST,
        }
        if action == "F":
            return (
                MoveTowardsWaypointInstruction(value)
                if relative_to_waypoint
                else MoveShipForwardInstruction(value)
            )
        elif action in directions:
            return (
                MoveWaypointInstruction(directions[action], value)
                if relative_to_waypoint
                else MoveShipInstruction(directions[action], value)
            )
        elif action in ("L", "R"):
            if value == 0:
                turn = TurnDirection.NO_TURN
            elif value == 90:
                turn = TurnDirection.LEFT if action == "L" else TurnDirection.RIGHT
            elif value == 180:
                turn = TurnDirection.U_TURN
            elif value == 270:
                turn = TurnDirection.RIGHT if action == "L" else TurnDirection.LEFT
            else:
                raise ValueError(f"Invalid turn angle: {value}")
            return (
                RotateWaypointInstruction(turn)
                if relative_to_waypoint
                else TurnShipInstruction(turn)
            )
        else:
            raise ValueError(f"Unknown navigation instruction: {instruction}")

    def parse_navigation_instructions(
        self, file_name: str, relative_to_waypoint: bool = False
    ) -> Iterator[NavigationInstruction]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield self._parse_navigation_instruction(
                    line.strip(), relative_to_waypoint
                )

    def parse_bus_schedules_and_current_timestamp(
        self, file_name: str
    ) -> tuple[list[BusSchedule], int]:
        lines = list(self._file_reader.readlines(file_name))
        current_timestamp = int(lines[0].strip())
        bus_schedules = [
            BusSchedule(index_in_list=i, bus_id=int(bus_id))
            for i, bus_id in enumerate(lines[1].strip().split(","))
            if bus_id != "x"
        ]
        return bus_schedules, current_timestamp

    @staticmethod
    def _parse_bitmask_instruction(
        instruction: str, is_address_mask: bool
    ) -> BitmaskInstruction:
        parts = instruction.split(" = ")
        if "mask" in parts[0]:
            return SetMaskInstruction(parts[1], is_address_mask)
        else:
            return WriteToMemoryInstruction(
                address=int(parts[0].replace("mem[", "").replace("]", "")),
                value=int(parts[1]),
            )

    def parse_bitmask_instructions(
        self, file_name: str, is_address_mask: bool
    ) -> Iterator[BitmaskInstruction]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield self._parse_bitmask_instruction(line.strip(), is_address_mask)

    @staticmethod
    def _parse_ticket_field_validator(line: str) -> TicketFieldValidator:
        parts = line.split(": ")
        field_name = parts[0]
        ranges = []
        for part in parts[1].split(" or "):
            min_value, max_value = map(int, part.split("-"))
            ranges.append(RangeInterval(min_value, max_value))
        return TicketFieldValidator(field_name, tuple(ranges))

    def parse_ticket_validator_and_ticket_values(
        self, file_name: str
    ) -> _ParsedTicketValidator:
        document_section = 0
        field_validators = []
        my_ticket = None
        nearby_tickets = []

        lines = list(self._file_reader.readlines(file_name))

        for line in lines:
            if not line.strip():
                continue
            if "your ticket" in line:
                document_section += 1
            elif "nearby tickets" in line:
                document_section += 1
            elif document_section == 0:
                field_validators.append(
                    self._parse_ticket_field_validator(line.strip())
                )
            elif document_section == 1:
                my_ticket = tuple(map(int, line.strip().split(",")))
            elif document_section == 2:
                nearby_tickets.append(tuple(map(int, line.strip().split(","))))
            else:
                raise ValueError(f"Unknown document section: {document_section}")

        return _ParsedTicketValidator(
            TicketValidator(tuple(field_validators)), my_ticket, nearby_tickets
        )

    def parse_context_free_grammar_and_words(
        self, file_name: str, starting_symbol: Hashable
    ) -> tuple[ContextFreeGrammar, list[str]]:
        cfg = ContextFreeGrammar(starting_symbol)
        words = []
        lines = list(self._file_reader.readlines(file_name))
        for line in lines:
            if ":" in line:
                parts = line.split(":")
                symbol = int(parts[0])
                for production in parts[1].split("|"):
                    if '"' in production:
                        terminal = production.strip().replace('"', "")
                        cfg.add_rule(symbol, production=(terminal,))
                    else:
                        cfg.add_rule(
                            symbol, production=tuple(map(int, production.split()))
                        )
            elif line.strip():
                words.append(line.strip())
        return cfg, words

    def parse_jigsaw_pieces(self, file_name: str) -> Iterator[JigsawPieceBinaryImage]:
        lines = list(self._file_reader.readlines(file_name))
        current_id = -1
        current_rows = []
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            if "Tile" in stripped_line:
                if current_id != -1:
                    yield JigsawPieceBinaryImage.from_string(current_id, current_rows)
                current_id = int(stripped_line.split(" ")[1].replace(":", ""))
                current_rows = []
            else:
                current_rows.append(stripped_line)
        if current_id != -1:
            yield JigsawPieceBinaryImage.from_string(current_id, current_rows)

    def _parse_food(self, line: str) -> Food:
        parts = line.split(" (contains ")
        ingredients = parts[0].split()
        allergens = parts[1].replace(")", "").split(", ")
        return Food(set(ingredients), set(allergens))

    def parse_foods(self, file_name: str) -> Iterator[Food]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield self._parse_food(line.strip())

    def parse_crab_combat_cards(self, file_name: str) -> tuple[list[int], list[int]]:
        cards_a = []
        cards_b = []
        reading_player_b = False
        for line in self._file_reader.readlines(file_name):
            if "Player 1" in line:
                reading_player_b = False
            elif "Player 2" in line:
                reading_player_b = True
            elif line.strip():
                if reading_player_b:
                    cards_b.append(int(line.strip()))
                else:
                    cards_a.append(int(line.strip()))
        return cards_a, cards_b

    def _parse_rotated_hexagonal_directions_without_delimiters(
        self, line: str
    ) -> Iterator[HexagonalDirection]:
        coord_map = {
            "se": HexagonalDirection.SOUTHEAST,
            "sw": HexagonalDirection.SOUTH,
            "nw": HexagonalDirection.NORTHWEST,
            "ne": HexagonalDirection.NORTH,
            "e": HexagonalDirection.NORTHEAST,
            "w": HexagonalDirection.SOUTHWEST,
        }
        current_idx = 0
        while current_idx < len(line):
            if line[current_idx] in coord_map:
                yield coord_map[line[current_idx]]
                current_idx += 1
            else:
                yield coord_map[line[current_idx : current_idx + 2]]
                current_idx += 2

    def parse_rotated_hexagonal_directions(
        self, file_name: str
    ) -> Iterator[list[HexagonalDirection]]:
        for line in self._file_reader.readlines(file_name):
            if line.strip():
                yield list(
                    self._parse_rotated_hexagonal_directions_without_delimiters(
                        line.strip()
                    )
                )
