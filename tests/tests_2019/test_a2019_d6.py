from models.aoc_2019 import CelestialBody


def test_celestial_body_starts_with_no_satellites():
    body = CelestialBody("COM")
    assert list(body.satellites) == []


def test_can_add_satellites_to_celestial_body():
    body = CelestialBody("COM")
    body.add_satellite(CelestialBody("A"))
    body.add_satellite(CelestialBody("B"))
    assert [satellite.name for satellite in body.satellites] == ["A", "B"]


def test_can_count_number_of_direct_and_indirect_orbits():
    com = CelestialBody("COM")
    a = CelestialBody("A")
    b = CelestialBody("B")
    c = CelestialBody("C")
    com.add_satellite(a)
    com.add_satellite(b)
    a.add_satellite(c)
    assert com.count_orbits() == 4
    assert a.count_orbits() == 1
    assert b.count_orbits() == 0
    assert c.count_orbits() == 0
