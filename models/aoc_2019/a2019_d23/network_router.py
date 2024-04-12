from .network_packet import NetworkPacket
from .network_input import NetworkInput


class NetworkRouter:
    def __init__(self, num_computers: int) -> None:
        self._network_inputs = [
            NetworkInput(address=address) for address in range(num_computers)
        ]
        self._lost_packages = []

    def send(self, packet: NetworkPacket) -> None:
        if packet.destination_address < 0 or packet.destination_address >= len(
            self._network_inputs
        ):
            self._lost_packages.append(packet)
            raise self.BadSendAddressError("Destination address out of range")
        self._network_inputs[packet.destination_address].enqueue(packet)

    def network_input(self, address: int) -> NetworkInput:
        if address < 0 or address >= len(self._network_inputs):
            raise IndexError("Computer address out of range")
        return self._network_inputs[address]

    @property
    def lost_packages(self) -> list[NetworkPacket]:
        return self._lost_packages

    class BadSendAddressError(Exception):
        pass
