from .network_packet import NetworkPacket


class LostPackets:
    def __init__(self, max_repeated_y_sent: int = 1) -> None:
        self._last_packet = None
        self._received_packet = False
        self._monitor = _LostPacketsMonitor(max_repeated_y_sent)

    @property
    def received_packet(self) -> bool:
        return self._received_packet

    def store(self, packet: NetworkPacket) -> None:
        self._received_packet = True
        self._last_packet = NetworkPacket(destination_address=0, content=packet.content)

    def last_packet(self) -> NetworkPacket:
        if self._last_packet is None:
            raise ValueError("No packets have been lost")
        self._monitor.store(self._last_packet)
        return self._last_packet

    @property
    def y_value_last_packet(self) -> int:
        return self._last_packet.content.y


class _LostPacketsMonitor:
    def __init__(self, max_repeated_y: int) -> None:
        self._last_y_value = None
        self._same_y_counter = 0
        self._max_repeated_y = max_repeated_y

    def store(self, packet: NetworkPacket) -> None:
        if packet.content.y == self._last_y_value:
            self._same_y_counter += 1
            if self._same_y_counter > self._max_repeated_y:
                raise OverflowError("Too many packets sent with the same y value")
        else:
            self._same_y_counter = 1
            self._last_y_value = packet.content.y

    def repeated_y_in_a_row(self) -> int:
        return self._same_y_counter
