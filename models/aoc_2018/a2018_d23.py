from dataclasses import dataclass
from models.vectors import Vector3D


@dataclass(frozen=True)
class TeleportNanobot:
    radius: int
    position: Vector3D

    @property
    def min_dist_to_origin(self) -> int:
        return max(0, self.position.manhattan_size - self.radius)

    @property
    def max_dist_to_origin(self) -> int:
        return self.position.manhattan_size + self.radius + 1

    def is_in_range(self, other_position: Vector3D) -> bool:
        return self.position.manhattan_distance(other_position) <= self.radius


@dataclass(frozen=True, order=True)
class _BotIncrement:
    dist_to_origin: int
    increment: int


def distance_of_position_with_strongest_signal(
    nanobots: list[TeleportNanobot],
) -> Vector3D:
    count_up_intervals = [
        _BotIncrement(bot.min_dist_to_origin, increment=1) for bot in nanobots
    ]
    count_down_intervals = [
        _BotIncrement(bot.max_dist_to_origin, increment=-1) for bot in nanobots
    ]
    intervals = sorted(count_up_intervals + count_down_intervals)
    num_bots_in_range = 0
    max_num_bots_in_range = 0
    optimal_distance = 0
    for interval in intervals:
        num_bots_in_range += interval.increment
        if num_bots_in_range > max_num_bots_in_range:
            optimal_distance = interval.dist_to_origin
            max_num_bots_in_range = num_bots_in_range
    return optimal_distance
