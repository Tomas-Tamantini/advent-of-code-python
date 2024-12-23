from models.common.io import InputFromString

from ..parser import parse_connections


def test_parse_connections():
    file_content = """go-ei
                      qp-pn
                      cf-qk"""
    input_reader = InputFromString(file_content)
    connections = list(parse_connections(input_reader))
    assert connections == [("go", "ei"), ("qp", "pn"), ("cf", "qk")]
