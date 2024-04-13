from .network_packet import NetworkPacket


class LostPackets:
    def __init__(self) -> None:
        self._last_packet = None

    def store(self, packet: NetworkPacket) -> None:
        self._last_packet = NetworkPacket(destination_address=0, content=packet.content)

    def last_packet(self) -> NetworkPacket:
        if self._last_packet is None:
            raise ValueError("No packets have been lost")
        return self._last_packet
