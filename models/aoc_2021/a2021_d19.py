from dataclasses import dataclass
from typing import Iterator, Optional
from collections import defaultdict
from models.vectors import Vector3D, Orientation
from models.common.io import ProgressBar


@dataclass(frozen=True)
class UnderwaterScanner:
    scanner_id: int
    visible_beacons_relative_coordinates: tuple[Vector3D]


@dataclass(frozen=True)
class PinpointedScanner:
    scanner_id: int
    visible_beacons_relative_coordinates: tuple[Vector3D]
    position: Vector3D
    orientation: Orientation

    def visible_beacons_absolute_coordinates(self) -> Iterator[Vector3D]:
        for beacon in self.visible_beacons_relative_coordinates:
            yield self.position + self.orientation.to_absolute_coordinates(beacon)

    def _most_common_offset(
        self, other: UnderwaterScanner, orientation: Orientation
    ) -> tuple[Vector3D, int]:
        offset_count = defaultdict(int)
        for my_beacon in self.visible_beacons_absolute_coordinates():
            for other_beacon in other.visible_beacons_relative_coordinates:
                transformed_other_beacon = orientation.to_absolute_coordinates(
                    other_beacon
                )
                offset_count[my_beacon - transformed_other_beacon] += 1
        most_common_offset = max(offset_count, key=offset_count.get)
        return most_common_offset, offset_count[most_common_offset]

    def pinpoint(
        self, other: UnderwaterScanner, min_num_matching_beacons: int
    ) -> Optional["PinpointedScanner"]:
        for orientation in Orientation.all_orientations_aligned_with_grid_axes():
            most_common_offset, offset_count = self._most_common_offset(
                other, orientation
            )
            if offset_count >= min_num_matching_beacons:
                return PinpointedScanner(
                    scanner_id=other.scanner_id,
                    position=most_common_offset,
                    orientation=orientation,
                    visible_beacons_relative_coordinates=other.visible_beacons_relative_coordinates,
                )


def pinpoint_scanners(
    scanners: list[UnderwaterScanner],
    min_num_matching_beacons: int,
    progress_bar: Optional[ProgressBar] = None,
) -> list[PinpointedScanner]:
    if not scanners:
        return []
    reference_scanner = scanners[0]
    reference_scanner = PinpointedScanner(
        scanner_id=reference_scanner.scanner_id,
        visible_beacons_relative_coordinates=reference_scanner.visible_beacons_relative_coordinates,
        position=Vector3D(0, 0, 0),
        orientation=Orientation(x_prime=Vector3D(1, 0, 0), y_prime=Vector3D(0, 1, 0)),
    )
    pinpointed_scanners = [reference_scanner]
    remaining_scanners = scanners[1:]
    bad_pairs = set()
    while remaining_scanners:
        if progress_bar:
            progress_bar.update(len(scanners) - len(remaining_scanners), len(scanners))
        new_pinpointed, scanner_to_remove = _pinpoint_new_scanner(
            min_num_matching_beacons, pinpointed_scanners, remaining_scanners, bad_pairs
        )
        pinpointed_scanners.append(new_pinpointed)
        remaining_scanners.remove(scanner_to_remove)

    return pinpointed_scanners


def _pinpoint_new_scanner(
    min_num_matching_beacons: int,
    pinpointed_scanners: list[PinpointedScanner],
    remaining_scanners: list[UnderwaterScanner],
    bad_pairs: set[tuple[PinpointedScanner, UnderwaterScanner]],
) -> tuple[PinpointedScanner, UnderwaterScanner]:
    for remaining_scanner in remaining_scanners:
        for pinpointed_scanner in pinpointed_scanners:
            if (pinpointed_scanner, remaining_scanner) in bad_pairs:
                continue
            new_pinpointed = pinpointed_scanner.pinpoint(
                remaining_scanner, min_num_matching_beacons
            )
            if new_pinpointed is None:
                bad_pairs.add((pinpointed_scanner, remaining_scanner))
            else:
                return new_pinpointed, remaining_scanner
