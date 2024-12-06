from typing import Protocol

from .network_packet import NetworkPacket


class HaltNetworkError(Exception):
    pass


class PacketMonitor(Protocol):
    def on_store_lost_packet(self, packet: NetworkPacket) -> None: ...

    def on_load_lost_packet(self, packet: NetworkPacket) -> None: ...


class MonitorBadAddressPackets:
    @staticmethod
    def on_store_lost_packet(packet: NetworkPacket) -> None:
        raise HaltNetworkError("Bad address packet stored")

    @staticmethod
    def on_load_lost_packet(packet: NetworkPacket) -> None:
        raise HaltNetworkError("Bad address packet loaded")


class MonitorRepeatedYValuePackets:
    def __init__(self, max_repeated_y: int) -> None:
        self._last_y_value = None
        self._same_y_counter = 0
        self._max_repeated_y = max_repeated_y

    def on_store_lost_packet(self, packet: NetworkPacket) -> None: ...

    def on_load_lost_packet(self, packet: NetworkPacket) -> None:
        if packet.content.y == self._last_y_value:
            self._same_y_counter += 1
            if self._same_y_counter > self._max_repeated_y:
                raise HaltNetworkError("Too many packets sent with the same y value")
        else:
            self._same_y_counter = 1
            self._last_y_value = packet.content.y
