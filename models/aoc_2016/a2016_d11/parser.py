from typing import Iterator

from models.common.io import InputReader

from .radio_isotope import FloorConfiguration


def _parse_floor_configuration(line: str) -> FloorConfiguration:
    parts = line.strip().split(" ")
    microchips = []
    generators = []
    for i, part in enumerate(parts):
        if "generator" in part:
            generators.append(parts[i - 1].strip())
        elif "microchip" in part:
            microchips.append(parts[i - 1].replace("-compatible", "").strip())
    return FloorConfiguration(tuple(microchips), tuple(generators))


def parse_radioisotope_testing_facility_floor_configurations(
    input_reader: InputReader,
) -> Iterator[FloorConfiguration]:
    for line in input_reader.readlines():
        yield _parse_floor_configuration(line)
