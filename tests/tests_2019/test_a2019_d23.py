import pytest
from unittest import mock
from typing import Optional
from models.vectors import Vector2D
from models.aoc_2019.a2019_d23 import (
    NetworkPacket,
    NetworkInput,
    NetworkRouter,
    NetworkOutput,
    run_network,
    LostPackets,
    PacketMonitor,
    HaltNetworkError,
    MonitorBadAddressPackets,
    MonitorRepeatedYValuePackets,
)


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


def test_network_input_is_not_idle_if_there_are_packets_to_read():
    network_input = NetworkInput(address=0)
    network_input.read()
    network_input.enqueue(
        NetworkPacket(destination_address=0, content=Vector2D(x=123, y=456))
    )
    assert not network_input.is_idle()


def test_network_input_is_not_idle_if_last_read_was_not_from_empty_queue():
    network_input = NetworkInput(address=0)
    network_input.read()
    assert not network_input.is_idle()


def test_network_input_is_idle_if_queue_is_empty_and_last_3_reads_were_from_empty_queue():
    network_input = NetworkInput(address=0)
    for _ in range(4):
        assert not network_input.is_idle()
        network_input.read()
    assert network_input.is_idle()


def _lost_packets(monitor: Optional[PacketMonitor] = None) -> LostPackets:
    if not monitor:
        monitor = mock.Mock()
    return LostPackets(monitor)


def test_lost_packets_manager_stores_last_packet_it_received():
    lost_packets = _lost_packets()
    content = Vector2D(x=123, y=456)
    packet = NetworkPacket(destination_address=7, content=content)
    lost_packets.store(packet)
    assert lost_packets.load_last_packet().content == content


def test_lost_packets_manager_overwrites_destination_address_to_zero():
    lost_packets = _lost_packets()
    packet = NetworkPacket(destination_address=7, content=Vector2D(x=123, y=456))
    lost_packets.store(packet)
    assert lost_packets.load_last_packet().destination_address == 0


def test_trying_to_fetch_lost_packet_when_none_was_stored_raises_error():
    lost_packets = _lost_packets()
    with pytest.raises(ValueError):
        lost_packets.load_last_packet()


def test_lost_packets_manager_informs_packets_stored_and_loaded_to_monitor():
    mock_monitor = mock.Mock()
    lost_packets = LostPackets(mock_monitor)
    content = Vector2D(x=123, y=456)
    packet = NetworkPacket(destination_address=7, content=content)
    expected_packet = NetworkPacket(destination_address=0, content=content)
    lost_packets.store(packet)
    assert mock_monitor.on_store_lost_packet.call_count == 1
    assert mock_monitor.on_store_lost_packet.call_args == mock.call(expected_packet)
    loaded_packet = lost_packets.load_last_packet()
    assert mock_monitor.on_load_lost_packet.call_count == 1
    assert mock_monitor.on_load_lost_packet.call_args == mock.call(expected_packet)
    assert loaded_packet == expected_packet


def test_bad_address_monitor_raises_halt_error_when_packet_is_stored_in_lost_packets_manager():
    monitor = MonitorBadAddressPackets()
    with pytest.raises(HaltNetworkError):
        monitor.on_store_lost_packet(
            NetworkPacket(destination_address=7, content=Vector2D(0, 0))
        )
    with pytest.raises(HaltNetworkError):
        monitor.on_load_lost_packet(
            NetworkPacket(destination_address=7, content=Vector2D(0, 0))
        )


def test_repeated_y_value_monitor_raises_halt_error_when_too_many_repeated_y_values_are_read():
    monitor = MonitorRepeatedYValuePackets(max_repeated_y=3)
    monitor.on_load_lost_packet(
        NetworkPacket(destination_address=0, content=Vector2D(0, 2))
    )
    monitor.on_load_lost_packet(
        NetworkPacket(destination_address=0, content=Vector2D(1, 2))
    )
    monitor.on_load_lost_packet(
        NetworkPacket(destination_address=0, content=Vector2D(2, 2))
    )
    with pytest.raises(HaltNetworkError):
        monitor.on_load_lost_packet(
            NetworkPacket(destination_address=0, content=Vector2D(3, 2))
        )


def test_network_router_creates_one_input_for_each_computer():
    router = NetworkRouter(num_computers=3, lost_packets_manager=_lost_packets())
    assert router.network_input(address=0) is not None
    assert router.network_input(address=1) is not None
    assert router.network_input(address=2) is not None
    with pytest.raises(IndexError):
        router.network_input(address=3)


def test_network_router_sends_packet_to_proper_address():
    router = NetworkRouter(num_computers=3, lost_packets_manager=_lost_packets())
    router.send(NetworkPacket(destination_address=1, content=Vector2D(x=10, y=20)))
    router.send(NetworkPacket(destination_address=2, content=Vector2D(x=30, y=40)))
    router.send(NetworkPacket(destination_address=1, content=Vector2D(x=50, y=60)))
    assert router.network_input(address=0).read() == 0
    assert router.network_input(address=0).read() == -1
    assert router.network_input(address=1).read() == 1
    assert router.network_input(address=1).read() == 10
    assert router.network_input(address=1).read() == 20
    assert router.network_input(address=1).read() == 50
    assert router.network_input(address=1).read() == 60
    assert router.network_input(address=1).read() == -1
    assert router.network_input(address=2).read() == 2
    assert router.network_input(address=2).read() == 30
    assert router.network_input(address=2).read() == 40
    assert router.network_input(address=2).read() == -1


def test_network_router_stores_packet_with_bad_address_in_lost_packet_manager():
    lost_packets = _lost_packets()
    router = NetworkRouter(num_computers=3, lost_packets_manager=lost_packets)
    content = Vector2D(x=10, y=20)
    packet = NetworkPacket(destination_address=3, content=content)
    router.send(packet)
    assert lost_packets.load_last_packet() == NetworkPacket(
        destination_address=0, content=content
    )


def test_network_sends_last_lost_packet_to_computer_zero():
    router = NetworkRouter(num_computers=3, lost_packets_manager=_lost_packets())
    content = Vector2D(x=10, y=20)
    packet = NetworkPacket(destination_address=3, content=content)
    router.send(packet)
    router.resend_lost_packet()
    assert router.network_input(address=0).read() == 0
    assert router.network_input(address=0).read() == 10
    assert router.network_input(address=0).read() == 20
    assert router.network_input(address=0).read() == -1


def test_network_is_idle_if_all_inputs_are_idle():
    router = NetworkRouter(num_computers=3, lost_packets_manager=_lost_packets())
    assert not router.is_idle()
    for address in range(3):
        for _ in range(4):
            router.network_input(address).read()
    assert router.is_idle()


def test_network_output_builds_packets_and_sends_them_to_router():
    router = NetworkRouter(num_computers=3, lost_packets_manager=_lost_packets())
    network_output = NetworkOutput(router=router)

    network_output.write(2)
    network_output.write(10)
    network_output.write(20)

    network_output.write(1)
    network_output.write(30)
    network_output.write(40)

    network_output.write(2)
    network_output.write(50)
    network_output.write(60)

    assert router.network_input(address=2).read() == 2
    assert router.network_input(address=2).read() == 10
    assert router.network_input(address=2).read() == 20
    assert router.network_input(address=2).read() == 50
    assert router.network_input(address=2).read() == 60
    assert router.network_input(address=2).read() == -1

    assert router.network_input(address=1).read() == 1
    assert router.network_input(address=1).read() == 30
    assert router.network_input(address=1).read() == 40
    assert router.network_input(address=1).read() == -1

    assert router.network_input(address=0).read() == 0
    assert router.network_input(address=0).read() == -1


def test_network_computers_run_identical_intcode_program_until_bad_address():
    # Program: Each computer gets its address as input, then output packet to address + 1. Last one should crash network.
    instructions = [
        3,  # Save address at #100
        100,
        101,  # Save address + 1 at #101
        1,
        100,
        101,
        102,  # Save address*10 at #102
        10,
        100,
        102,
        102,  # Save address*20 at #103
        20,
        100,
        103,
        4,  # Output packet destination, x and y
        101,
        4,
        102,
        4,
        103,
        99,
    ]
    lost_packets = LostPackets(monitor=MonitorBadAddressPackets())
    run_network(
        num_computers=3, lost_packets_manager=lost_packets, instructions=instructions
    )
    assert lost_packets.content_last_packet == Vector2D(x=20, y=40)


def test_network_computers_run_identical_intcode_program_until_overflow_of_lost_packets_with_same_y_value():
    # Program: Each computer gets its address as input, then output packet to address + 1. Last one should go to lost packets.
    instructions = [
        3,  # Save address at #100
        100,
        101,  # Save address + 1 at #101
        1,
        100,
        101,
        102,  # Save address*10 at #102
        10,
        100,
        102,
        102,  # Save address*20 at #103
        20,
        100,
        103,
        4,  # Output packet destination, x and y
        101,
        4,
        102,
        4,
        103,
    ]
    instructions += [3, 1000] * 10 + [99]  # A few inputs to reach idle state
    lost_packets = LostPackets(monitor=MonitorRepeatedYValuePackets(max_repeated_y=1))
    run_network(
        num_computers=3, lost_packets_manager=lost_packets, instructions=instructions
    )
    assert lost_packets.content_last_packet == Vector2D(x=20, y=40)
