from models.common.io import InputFromString
from ..parser import parse_bridge_components
from ..bridge_builder import BridgeComponent


def test_parse_bridge_components():
    file_content = """0/2
                      3/1"""
    components = list(parse_bridge_components(InputFromString(file_content)))
    assert components == [BridgeComponent(0, 2), BridgeComponent(3, 1)]
