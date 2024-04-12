import pytest
from models.vectors import Vector2D
from models.aoc_2019.a2019_d23 import NetworkPacket, NetworkInput


def test_network_input_first_informs_computer_address():
    network_input = NetworkInput(address=123)
    assert network_input.read() == 123


def test_empty_network_input_returns_minus_one():
    network_input = NetworkInput(address=123)
    network_input.read()
    assert network_input.read() == -1


def test_network_input_informs_received_packets_x_and_y_in_order():
    network_input = NetworkInput(address=123)
    network_input.enqueue(
        NetworkPacket(destination_address=123, content=Vector2D(x=10, y=20))
    )
    assert network_input.read() == 123
    assert network_input.read() == 10
    assert network_input.read() == 20


def test_network_input_raises_value_error_if_packet_received_has_different_address():
    network_input = NetworkInput(address=123)
    with pytest.raises(ValueError):
        network_input.enqueue(
            NetworkPacket(destination_address=321, content=Vector2D(x=10, y=20))
        )


def test_network_input_enqueues_received_packets():
    network_input = NetworkInput(address=0)
    network_input.enqueue(
        NetworkPacket(destination_address=0, content=Vector2D(x=123, y=456))
    )
    network_input.enqueue(
        NetworkPacket(destination_address=0, content=Vector2D(x=789, y=101112))
    )
    expected_read_values = [0, 123, 456, 789, 101112, -1]
    assert all(
        network_input.read() == expected_value
        for expected_value in expected_read_values
    )
