from models.vectors import Vector2D
from models.aoc_2019.a2019_d17 import ScaffoldMap, CameraOutput, run_scaffolding_program


def test_scaffold_map_starts_empty():
    sm = ScaffoldMap()
    assert sm.render() == ""


def test_can_add_pixels_to_scaffold_map():
    sm = ScaffoldMap()
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("v")
    sm.add_pixel("\n")
    sm.add_pixel("#")
    sm.add_pixel("#")
    sm.add_pixel("#")

    assert sm.render() == "#.v\n###"


def test_can_iterate_through_scaffolding_intersections():
    sm = ScaffoldMap()
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("\n")
    sm.add_pixel("#")
    sm.add_pixel("#")
    sm.add_pixel("#")
    sm.add_pixel("#")
    sm.add_pixel("\n")
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("\n")

    assert list(sm.scaffolding_intersections()) == [Vector2D(0, 1), Vector2D(2, 1)]


def test_camera_output_converts_value_to_ascii_and_builds_map():
    sm = ScaffoldMap()
    co = CameraOutput(sm)
    co.write(35)
    co.write(46)
    co.write(118)
    co.write(10)
    co.write(35)
    co.write(35)
    co.write(35)

    assert sm.render() == "#.v\n###"


def test_can_run_scaffolding_program_to_build_map():
    instructions = [104, 35, 99]
    sm = ScaffoldMap()
    run_scaffolding_program(sm, instructions)
    assert sm.render() == "#"
