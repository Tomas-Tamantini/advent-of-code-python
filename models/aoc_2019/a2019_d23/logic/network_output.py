from models.common.vectors import Vector2D

from .network_packet import NetworkPacket
from .network_router import NetworkRouter


class NetworkOutput:
    def __init__(self, router: NetworkRouter) -> None:
        self._router = router
        self._buffer = []

    def _build_packet(self) -> NetworkPacket:
        return NetworkPacket(
            destination_address=self._buffer[0],
            content=Vector2D(x=self._buffer[1], y=self._buffer[2]),
        )

    def write(self, value: int) -> None:
        self._buffer.append(value)
        if len(self._buffer) == 3:
            self._router.send(self._build_packet())
            self._buffer = []
