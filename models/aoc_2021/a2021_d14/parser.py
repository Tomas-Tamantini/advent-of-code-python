from models.common.io import InputReader


def parse_polymer_and_polymer_extension_rules(
    input_reader: InputReader,
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
