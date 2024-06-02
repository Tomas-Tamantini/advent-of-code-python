from ..celestial_body import CelestialBody


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


def test_orbital_distance_between_two_bodies_is_min_num_steps_through_tree():
    com = CelestialBody("COM")
    a = CelestialBody("A")
    b = CelestialBody("B")
    c = CelestialBody("C")
    d = CelestialBody("D")

    com.add_satellite(a)
    com.add_satellite(b)
    b.add_satellite(c)
    b.add_satellite(d)

    assert com.orbital_distance("COM", "COM") == 0
    assert com.orbital_distance("COM", "A") == 1
    assert com.orbital_distance("C", "D") == 2
    assert com.orbital_distance("C", "A") == 3
