from models.common.vectors import Vector2D
from .network_packet import NetworkPacket
from .packet_monitor import PacketMonitor


class LostPackets:
    def __init__(self, monitor: PacketMonitor) -> None:
        self._last_packet = None
        self._monitor = monitor

    def store(self, packet: NetworkPacket) -> None:
        self._last_packet = NetworkPacket(destination_address=0, content=packet.content)
        self._monitor.on_store_lost_packet(self._last_packet)

    def load_last_packet(self) -> NetworkPacket:
        if self._last_packet is None:
            raise ValueError("No packets have been lost")
        self._monitor.on_load_lost_packet(self._last_packet)
        return self._last_packet

    @property
    def content_last_packet(self) -> Vector2D:
        return self._last_packet.content
