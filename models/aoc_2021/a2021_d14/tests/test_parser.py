from models.common.io import InputFromString

from ..parser import parse_polymer_and_polymer_extension_rules


def test_parse_polymer_and_polymer_extension_rules():
    file_content = """NNCB

                      CH -> B
                      HH -> N"""
    polymer, rules = parse_polymer_and_polymer_extension_rules(
        InputFromString(file_content)
    )
    assert polymer == "NNCB"
    assert rules == {
        "CH": "B",
        "HH": "N",
    }
