from dataclasses import dataclass


@dataclass(frozen=True)
class BusSchedule:
    index_in_list: int
    bus_id: int

    def wait_time(self, timestamp: int) -> int:
        return (self.bus_id - timestamp) % self.bus_id
