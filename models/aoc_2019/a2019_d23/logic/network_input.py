from queue import Queue
from .network_packet import NetworkPacket


class NetworkInput:
    def __init__(self, address: int) -> None:
        self._address = address
        self._is_first_read = False
        self._queue = Queue()
        self._num_reads_from_empty_queue = 0

    def enqueue(self, packet: NetworkPacket) -> None:
        if packet.destination_address != self._address:
            raise ValueError("Packet received has different address")
        self._queue.put(packet.content.x)
        self._queue.put(packet.content.y)

    def read(self) -> int:
        if not self._is_first_read:
            self._is_first_read = True
            return self._address
        elif self._queue.empty():
            self._num_reads_from_empty_queue += 1
            return -1
        else:
            self._num_reads_from_empty_queue = 0
            return self._queue.get()

    def is_idle(self) -> bool:
        return self._queue.empty() and self._num_reads_from_empty_queue > 2
