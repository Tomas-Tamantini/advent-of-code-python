from models.common.io import InputFromString

from ..parser import parse_layered_firewall


def test_parse_layered_firewall():
    file_content = """0: 3
                      1: 2
                      4: 4
                      6: 4"""
    firewall = parse_layered_firewall(InputFromString(file_content))
    assert [layer for layer, _ in firewall.packet_collisions()] == [0, 6]
