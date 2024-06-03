from typing import Iterator, Hashable

import numpy as np
from collections import defaultdict
from models.common.io import InputReader

from models.common.vectors import (
    CardinalDirection,
    Vector2D,
    Vector3D,
    BoundingBox,
)
from models.common.assembly import Instruction, ContextFreeGrammar
from models.aoc_2020 import (
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
    JigsawPieceBinaryImage,
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


class FileParser:

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
