from models.common.vectors import Vector3D, solve_linear_system_exactly
from .hailstone import Hailstone


def _linear_system_matrix(hailstones: list[Hailstone]) -> list[list[int]]:
    a_0 = hailstones[0].velocity - hailstones[1].velocity
    a_1 = hailstones[0].velocity - hailstones[2].velocity

    b_0 = hailstones[1].position - hailstones[0].position
    b_1 = hailstones[2].position - hailstones[0].position

    return [
        [0, -a_0.z, a_0.y, 0, -b_0.z, b_0.y],
        [a_0.z, 0, -a_0.x, b_0.z, 0, -b_0.x],
        [-a_0.y, a_0.x, 0, -b_0.y, b_0.x, 0],
        [0, -a_1.z, a_1.y, 0, -b_1.z, b_1.y],
        [a_1.z, 0, -a_1.x, b_1.z, 0, -b_1.x],
        [-a_1.y, a_1.x, 0, -b_1.y, b_1.x, 0],
    ]


def _linear_system_vector(hailstones) -> list[int]:
    c_0 = hailstones[1].pos_vel_cross_product() - hailstones[0].pos_vel_cross_product()
    c_1 = hailstones[2].pos_vel_cross_product() - hailstones[0].pos_vel_cross_product()

    return [c_0.x, c_0.y, c_0.z, c_1.x, c_1.y, c_1.z]


def rock_that_hits_all_hailstones(hailstones: list[Hailstone]) -> Hailstone:
    a = _linear_system_matrix(hailstones)
    b = _linear_system_vector(hailstones)
    solution = solve_linear_system_exactly(a, b)
    int_solution = [int(solution[i]) for i in range(6)]
    return Hailstone(
        position=Vector3D(*int_solution[:3]), velocity=Vector3D(*int_solution[3:])
    )
