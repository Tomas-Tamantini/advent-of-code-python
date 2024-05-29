from models.common.io import InputReader


def parse_rpg_boss(input_reader: InputReader) -> dict[str, int]:
    attributes = {}
    for line in input_reader.readlines():
        parts = line.split(":")
        value = int(parts[-1])
        if "Hit Points" in line:
            attributes["hit_points"] = value
        elif "Damage" in line:
            attributes["damage"] = value
        elif "Armor" in line:
            attributes["armor"] = value
    return attributes
