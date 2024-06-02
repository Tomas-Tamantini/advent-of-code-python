from .network_packet import NetworkPacket
from .network_input import NetworkInput
from .lost_packets import LostPackets


class NetworkRouter:
    def __init__(self, num_computers: int, lost_packets_manager: LostPackets) -> None:
        self._network_inputs = [
            NetworkInput(address=address) for address in range(num_computers)
        ]
        self._lost_packets_manager = lost_packets_manager

    @property
    def num_computers(self) -> int:
        return len(self._network_inputs)

    def send(self, packet: NetworkPacket) -> None:
        if packet.destination_address < 0 or packet.destination_address >= len(
            self._network_inputs
        ):
            self._lost_packets_manager.store(packet)
        else:
            self._network_inputs[packet.destination_address].enqueue(packet)

    def network_input(self, address: int) -> NetworkInput:
        if address < 0 or address >= len(self._network_inputs):
            raise IndexError("Computer address out of range")
        return self._network_inputs[address]

    def is_idle(self) -> bool:
        return all(input.is_idle() for input in self._network_inputs)

    def resend_lost_packet(self) -> None:
        self.send(self._lost_packets_manager.load_last_packet())
