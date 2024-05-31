from models.common.io import InputFromString
from ..parser import parse_radioisotope_testing_facility_floor_configurations
from ..radio_isotope import FloorConfiguration


def test_parse_radioisotope_testing_facility_floor_configurations():
    file_content = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
                      The second floor contains a hydrogen generator.
                      The third floor contains a lithium generator.
                      The fourth floor contains nothing relevant."""
    floors = list(
        parse_radioisotope_testing_facility_floor_configurations(
            InputFromString(file_content)
        )
    )
    assert floors == [
        FloorConfiguration(("hydrogen", "lithium"), tuple()),
        FloorConfiguration(tuple(), ("hydrogen",)),
        FloorConfiguration(tuple(), ("lithium",)),
        FloorConfiguration(tuple(), tuple()),
    ]
