from models.common.io import InputFromString
from ..parser import parse_disc_system


def test_parse_disc_system():
    file_content = """Disc #1 has 5 positions; at time=0, it is at position 4.
                      Disc #2 has 2 positions; at time=0, it is at position 1."""
    disc_system = parse_disc_system(InputFromString(file_content))
    assert disc_system.time_to_press_button() == 5
