from typing import Iterator, Optional, Hashable
from dataclasses import dataclass
import numpy as np
from datetime import datetime
from collections import defaultdict
from models.common.io import InputReader, CharacterGrid
from models.common.graphs import DirectedGraph
from models.common.number_theory import Interval
from models.common.vectors import (
    CardinalDirection,
    Vector2D,
    TurnDirection,
    Vector3D,
    HexagonalDirection,
    BoundingBox,
)
from models.common.assembly import Instruction, ContextFreeGrammar
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
    JigsawPieceBinaryImage,
    Food,
)
from models.aoc_2021 import (
    SubmarineNavigationInstruction,
    MoveSubmarineInstruction,
    IncrementAimInstruction,
    MoveSubmarineWithAimInstruction,
    BingoBoard,
    BingoGame,
    LineSegment,
    ShuffledSevenDigitDisplay,
    UnderwaterCave,
    FoldInstruction,
    UnderwaterScanner,
    Cuboid,
    CuboidInstruction,
    Amphipod,
    AmphipodRoom,
    AmphipodHallway,
    AmphipodBurrow,
)


@dataclass
class _ParsedTicketValidator:
    validator: TicketValidator
    my_ticket: tuple[int]
    nearby_tickets: list[tuple[int]]


class FileParser:

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

    def parse_fabric_rectangles(
        self, input_reader: InputReader
    ) -> Iterator[FabricRectangle]:
        for line in input_reader.readlines():
            yield self._parse_fabric_rectangle(line)

    def parse_guard_logs(self, input_reader: InputReader) -> Iterator[Guard]:
        lines = [l.strip() for l in input_reader.readlines()]
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

    def parse_directed_graph(self, input_reader: InputReader) -> DirectedGraph:
        graph = DirectedGraph()
        for line in input_reader.readlines():
            parts = line.strip().split(" ")
            graph.add_edge(parts[1], parts[-3])
        return graph

    def parse_moving_particles(
        self, input_reader: InputReader
    ) -> Iterator[MovingParticle]:
        for line in input_reader.readlines():
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

    def parse_plant_automaton(self, input_reader: InputReader) -> PlantAutomaton:
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

    def parse_instruction_samples(
        self, input_reader: InputReader
    ) -> Iterator[InstructionSample]:
        lines = list(input_reader.readlines())
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
        input_reader: InputReader,
        op_code_to_instruction: dict[int, type[ThreeValueInstruction]],
    ) -> Iterator[ThreeValueInstruction]:
        instructions = []
        for line in reversed(list(input_reader.readlines())):
            if "After:" in line:
                break
            if not line.strip():
                continue
            values = list(map(int, line.strip().split()))
            op_code = values[0]
            instruction_type = op_code_to_instruction[op_code]
            instructions.append(instruction_type(*values[1:]))
        yield from reversed(instructions)

    def parse_position_ranges(self, input_reader: InputReader) -> Iterator[Vector2D]:
        for line in input_reader.readlines():
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
        self, input_reader: InputReader
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
        for line in input_reader.readlines():
            parts = line.strip().split()
            if "#ip" in parts:
                register_bound_to_pc = int(parts[-1])
            else:
                instruction_type = instruction_types[parts[0]]
                yield instruction_type(*map(int, parts[1:]), register_bound_to_pc)

    def parse_nanobots(self, input_reader: InputReader) -> Iterator[TeleportNanobot]:
        for line in input_reader.readlines():
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

    def parse_directions(
        self, input_reader: InputReader
    ) -> Iterator[list[tuple[CardinalDirection, int]]]:
        direction_dict = {
            "U": CardinalDirection.NORTH,
            "R": CardinalDirection.EAST,
            "D": CardinalDirection.SOUTH,
            "L": CardinalDirection.WEST,
        }

        for line in input_reader.readlines():
            yield [
                (direction_dict[part.strip()[0]], int(part.strip()[1:]))
                for part in line.strip().split(",")
            ]

    def parse_celestial_bodies(self, input_reader: InputReader) -> CelestialBody:
        bodies = dict()
        for line in input_reader.readlines():
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

    def parse_chemical_reactions(
        self, input_reader: InputReader
    ) -> Iterator[ChemicalReaction]:
        for line in input_reader.readlines():
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
        self, input_reader: InputReader, split_entrance_four_ways: bool = False
    ) -> TunnelMaze:
        content = input_reader.read()
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

    def parse_portal_maze(self, input_reader: InputReader) -> PortalMaze:
        portals = defaultdict(list)
        maze = PortalMaze()
        lines = list(input_reader.readlines())
        for position in self._open_passage_tiles(lines):
            maze.add_node_and_connect_to_neighbors(position)
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

    def parse_recursive_donut_maze(
        self, input_reader: InputReader
    ) -> RecursiveDonutMaze:
        portals = defaultdict(dict)
        maze = RecursiveDonutMaze()
        lines = list(input_reader.readlines())
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

    def parse_multi_technique_shuffle(
        self, input_reader: InputReader
    ) -> MultiTechniqueShuffle:
        techniques = []
        for line in input_reader.readlines():
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
        self, input_reader: InputReader, use_range_policy: bool
    ) -> Iterator[tuple[PasswordPolicy, str]]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_password_policy_and_password(line, use_range_policy)

    def parse_passports(self, input_reader: InputReader) -> Iterator[dict[str, str]]:
        passport = {}
        for line in input_reader.read_stripped_lines(keep_empty_lines=True):
            if line:
                parts = line.split()
                for part in parts:
                    key, value = part.split(":")
                    passport[key] = value
            else:
                if passport:
                    yield passport
                passport = {}
        if passport:
            yield passport

    def parse_plane_seat_ids(self, input_reader: InputReader) -> Iterator[int]:
        for line in input_reader.readlines():
            line = line.strip()
            if line:
                row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
                col = int(line[7:].replace("L", "0").replace("R", "1"), 2)
                yield row * 8 + col

    def parse_form_answers_by_groups(
        self, input_reader: InputReader
    ) -> Iterator[CustomsGroup]:
        current_group = CustomsGroup()
        for line in input_reader.read_stripped_lines(keep_empty_lines=True):
            if line:
                current_group.add_individual_answers(set(line))
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

    def parse_luggage_rules(self, input_reader: InputReader) -> LuggageRules:
        rules = LuggageRules()
        for line in input_reader.read_stripped_lines():
            rules.add_rule(self._parse_luggage_rule(line))
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

    def parse_game_console_instructions(
        self, input_reader: InputReader
    ) -> Iterator[Instruction]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_game_console_instruction(line)

    @staticmethod
    def _parse_navigation_instruction(
        instruction: str, relative_to_waypoint: bool
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
        self, input_reader: InputReader, relative_to_waypoint: bool = False
    ) -> Iterator[NavigationInstruction]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_navigation_instruction(line, relative_to_waypoint)

    def parse_bus_schedules_and_current_timestamp(
        self, input_reader: InputReader
    ) -> tuple[list[BusSchedule], int]:
        lines = list(input_reader.readlines())
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
        self, input_reader: InputReader, is_address_mask: bool
    ) -> Iterator[BitmaskInstruction]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_bitmask_instruction(line, is_address_mask)

    @staticmethod
    def _parse_ticket_field_validator(line: str) -> TicketFieldValidator:
        parts = line.split(": ")
        field_name = parts[0]
        ranges = []
        for part in parts[1].split(" or "):
            min_value, max_value = map(int, part.split("-"))
            ranges.append(Interval(min_value, max_value))
        return TicketFieldValidator(field_name, tuple(ranges))

    def parse_ticket_validator_and_ticket_values(
        self, input_reader: InputReader
    ) -> _ParsedTicketValidator:
        document_section = 0
        field_validators = []
        my_ticket = None
        nearby_tickets = []

        lines = list(input_reader.readlines())

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
        self, input_reader: InputReader, starting_symbol: Hashable
    ) -> tuple[ContextFreeGrammar, list[str]]:
        cfg = ContextFreeGrammar(starting_symbol)
        words = []
        lines = list(input_reader.read_stripped_lines())
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
            else:
                words.append(line)
        return cfg, words

    def parse_jigsaw_pieces(
        self, input_reader: InputReader
    ) -> Iterator[JigsawPieceBinaryImage]:
        lines = list(input_reader.readlines())
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

    @staticmethod
    def _parse_food(line: str) -> Food:
        parts = line.split(" (contains ")
        ingredients = parts[0].split()
        allergens = parts[1].replace(")", "").split(", ")
        return Food(set(ingredients), set(allergens))

    def parse_foods(self, input_reader: InputReader) -> Iterator[Food]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_food(line)

    def parse_crab_combat_cards(
        self, input_reader: InputReader
    ) -> tuple[list[int], list[int]]:
        cards_a = []
        cards_b = []
        reading_player_b = False
        for line in input_reader.read_stripped_lines():
            if "Player 1" in line:
                reading_player_b = False
            elif "Player 2" in line:
                reading_player_b = True
            else:
                if reading_player_b:
                    cards_b.append(int(line))
                else:
                    cards_a.append(int(line))
        return cards_a, cards_b

    @staticmethod
    def _parse_rotated_hexagonal_directions_without_delimiters(
        line: str,
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
        self, input_reader: InputReader
    ) -> Iterator[list[HexagonalDirection]]:
        for line in input_reader.read_stripped_lines():
            yield list(
                self._parse_rotated_hexagonal_directions_without_delimiters(line)
            )

    @staticmethod
    def _parse_navigation_instruction_for_submarine_without_aim(
        line: str,
    ) -> SubmarineNavigationInstruction:
        directions = {
            "forward": CardinalDirection.EAST,
            "up": CardinalDirection.NORTH,
            "down": CardinalDirection.SOUTH,
        }
        parts = line.split()
        return MoveSubmarineInstruction(directions[parts[0]], int(parts[1]))

    @staticmethod
    def _parse_navigation_instruction_for_submarine_with_aim(
        line: str,
    ) -> SubmarineNavigationInstruction:
        instruction, amount = line.split()
        amount = int(amount)
        if "down" in instruction:
            return IncrementAimInstruction(amount)
        elif "up" in instruction:
            return IncrementAimInstruction(-amount)
        elif "forward" in instruction:
            return MoveSubmarineWithAimInstruction(amount)
        else:
            raise ValueError(f"Unknown submarine navigation instruction: {line}")

    def parse_submarine_navigation_instructions(
        self, input_reader: InputReader, submarine_has_aim: bool
    ) -> Iterator[SubmarineNavigationInstruction]:
        for line in input_reader.read_stripped_lines():

            if submarine_has_aim:
                yield self._parse_navigation_instruction_for_submarine_with_aim(line)
            else:
                yield self._parse_navigation_instruction_for_submarine_without_aim(line)

    def parse_bingo_game_and_numbers_to_draw(
        self, input_reader: InputReader
    ) -> tuple[BingoGame, list[int]]:
        lines = list(input_reader.read_stripped_lines(keep_empty_lines=True))
        tables = []
        numbers_to_draw = []
        current_table = []
        for line in lines:
            if "," in line:
                numbers_to_draw = list(map(int, line.split(",")))
            elif line:
                current_table.append(list(map(int, line.split())))
            elif current_table:
                tables.append(current_table)
                current_table = []
        if current_table:
            tables.append(current_table)
        boards = (BingoBoard(np.array(board, dtype=np.int32)) for board in tables)
        return BingoGame(tuple(boards)), numbers_to_draw

    @staticmethod
    def _parse_line_segment(line: str) -> LineSegment:
        parts = line.split("->")
        start = Vector2D(*map(int, parts[0].split(",")))
        end = Vector2D(*map(int, parts[1].split(",")))
        return LineSegment(start, end)

    def parse_line_segments(self, input_reader: InputReader) -> Iterator[LineSegment]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_line_segment(line)

    @staticmethod
    def _parse_shuffled_seven_digit_display(line: str) -> ShuffledSevenDigitDisplay:
        parts = line.split("|")
        unique_patterns = tuple(x.strip() for x in parts[0].split())
        four_digit_output = tuple(x.strip() for x in parts[1].split())
        return ShuffledSevenDigitDisplay(unique_patterns, four_digit_output)

    def parse_shuffled_seven_digit_displays(
        self, input_reader: InputReader
    ) -> Iterator[ShuffledSevenDigitDisplay]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_shuffled_seven_digit_display(line)

    @staticmethod
    def _parse_underwater_caves(line: str) -> tuple[UnderwaterCave, UnderwaterCave]:
        return tuple(
            UnderwaterCave(name, is_small=name.islower())
            for name in [p.strip() for p in line.split("-")]
        )

    def parse_underwater_cave_connections(
        self, input_reader: InputReader
    ) -> dict[UnderwaterCave, set[UnderwaterCave]]:
        connections = defaultdict(set)
        for line in input_reader.read_stripped_lines():
            cave_a, cave_b = self._parse_underwater_caves(line)
            connections[cave_a].add(cave_b)

        return connections

    @staticmethod
    def _parse_fold_instruction(line: str) -> FoldInstruction:
        is_horizontal = "y" in line
        index = int(line.split("=")[1])
        return FoldInstruction(is_horizontal, index)

    def parse_positions_and_fold_instructions(
        self, input_reader: InputReader
    ) -> tuple[list[Vector2D], list[FoldInstruction]]:
        positions = []
        instructions = []
        for line in input_reader.read_stripped_lines():
            if "fold" in line:
                instructions.append(self._parse_fold_instruction(line))
            else:
                positions.append(Vector2D(*map(int, line.split(","))))
        return positions, instructions

    def parse_polymer_and_polymer_extension_rules(
        self, input_reader: InputReader
    ) -> tuple[str, dict[str, str]]:
        polymer = ""
        rules = dict()

        for line in input_reader.read_stripped_lines():
            if "->" in line:
                parts = line.split("->")
                rules[parts[0].strip()] = parts[1].strip()
            else:
                polymer = line

        return polymer, rules

    def parse_bounding_box(self, input_reader: InputReader) -> BoundingBox:
        """target area: x=244..303, y=-91..-54"""
        line = input_reader.read().strip()
        parts = line.split(",")
        x_parts = parts[0].split("=")[-1]
        y_parts = parts[1].split("=")[-1]
        x_min, x_max = map(int, x_parts.split(".."))
        y_min, y_max = map(int, y_parts.split(".."))
        return BoundingBox(
            bottom_left=Vector2D(x_min, y_min), top_right=Vector2D(x_max, y_max)
        )

    def parse_underwater_scanners(
        self, input_reader: InputReader
    ) -> Iterator[UnderwaterScanner]:
        current_positions = []
        current_scanner_id = -1
        for line in input_reader.read_stripped_lines():
            if "scanner" in line:
                if current_positions:
                    yield UnderwaterScanner(
                        current_scanner_id, tuple(current_positions)
                    )
                current_scanner_id = int(line.split()[2])
                current_positions = []
            else:
                current_positions.append(Vector3D(*map(int, line.split(","))))
        if current_positions:
            yield UnderwaterScanner(current_scanner_id, tuple(current_positions))

    def parse_trench_rules_and_trench_map(
        self, input_reader: InputReader
    ) -> tuple[set[int], set[Vector2D]]:
        trench_rules = set()
        trench_map = set()
        current_row = 0
        for line in input_reader.read_stripped_lines():
            active_columns = {i for i, c in enumerate(line) if c == "#"}
            if not trench_rules:
                trench_rules = active_columns
            else:
                trench_map.update(Vector2D(i, current_row) for i in active_columns)
                current_row += 1
        return trench_rules, trench_map

    def parse_players_starting_positions(
        self, input_reader: InputReader
    ) -> tuple[int, int]:
        lines = list(input_reader.readlines())
        return tuple(int(line.strip().split()[-1]) for line in lines)

    @staticmethod
    def _parse_cuboid_instruction(line: str) -> CuboidInstruction:
        parts = (
            line.replace("x", "")
            .replace("y", "")
            .replace("z", "")
            .replace(",", "")
            .replace("on", "")
            .replace("off", "")
            .split("=")
        )
        x_min, x_max = map(int, parts[1].split(".."))
        y_min, y_max = map(int, parts[2].split(".."))
        z_min, z_max = map(int, parts[3].split(".."))
        return CuboidInstruction(
            is_turn_on="on" in line,
            cuboid=Cuboid(
                range_start=Vector3D(x_min, y_min, z_min),
                range_end=Vector3D(x_max, y_max, z_max),
            ),
        )

    def parse_cuboid_instructions(
        self, input_reader: InputReader
    ) -> Iterator[CuboidInstruction]:
        for line in input_reader.read_stripped_lines():
            yield self._parse_cuboid_instruction(line)

    @staticmethod
    def _upper_case_letters(line: str) -> Iterator[tuple[int, chr]]:
        for i, letter in enumerate(line):
            if letter.isupper():
                yield i, letter

    @staticmethod
    def _amphipod_from_letter(letter: chr) -> Amphipod:
        room_index = ord(letter) - ord("A")
        return Amphipod(
            desired_room_index=room_index, energy_spent_per_step=10**room_index
        )

    def parse_amphipod_burrow(
        self, input_reader: InputReader, *insertions: str
    ) -> AmphipodBurrow:
        hallway_length = -1
        hallway_start_index = -1
        rooms_as_dict = defaultdict(list)
        for line in input_reader.readlines():
            if "." in line:
                hallway_length = line.count(".")
                hallway_start_index = line.index(".")
            else:
                for position, letter in self._upper_case_letters(line):
                    rooms_as_dict[position].insert(0, letter)
        hallway = AmphipodHallway(positions=tuple(None for _ in range(hallway_length)))
        rooms = []
        for room_index, (absolute_position, letters) in enumerate(
            sorted(rooms_as_dict.items())
        ):
            if room_index < len(insertions):
                letters = letters[:1] + list(insertions[room_index]) + letters[1:]
            amphipods = tuple(self._amphipod_from_letter(letter) for letter in letters)
            room = AmphipodRoom(
                index=room_index,
                capacity=len(letters),
                position_in_hallway=absolute_position - hallway_start_index,
                amphipods_back_to_front=amphipods,
            )
            rooms.append(room)
        return AmphipodBurrow(hallway, tuple(rooms))
