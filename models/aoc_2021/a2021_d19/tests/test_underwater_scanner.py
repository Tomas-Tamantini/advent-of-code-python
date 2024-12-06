from models.common.vectors import Orientation, Vector3D

from ..underwater_scanner import (
    PinpointedScanner,
    UnderwaterScanner,
    pinpoint_scanners,
)


def test_underwater_scanner_converts_relative_to_absolute_coordinates():
    scanner = PinpointedScanner(
        scanner_id=0,
        position=Vector3D(10, 20, 30),
        orientation=Orientation(x_prime=Vector3D(0, 0, -1), y_prime=Vector3D(1, 0, 0)),
        visible_beacons_relative_coordinates=[Vector3D(1, 2, 3)],
    )
    assert list(scanner.visible_beacons_absolute_coordinates()) == [
        Vector3D(12, 17, 29)
    ]


def _reference_scanner(visible_beacons_relative_coordinates):
    return PinpointedScanner(
        scanner_id=0,
        position=Vector3D(0, 0, 0),
        orientation=Orientation(x_prime=Vector3D(1, 0, 0), y_prime=Vector3D(0, 1, 0)),
        visible_beacons_relative_coordinates=visible_beacons_relative_coordinates,
    )


def test_underwater_scanner_cannot_pinpoint_other_scanner_if_less_than_appropriate_number_of_beacons_align():
    reference_scanner = _reference_scanner(
        visible_beacons_relative_coordinates=[
            Vector3D(0, 2, 0),
            Vector3D(4, 1, 0),
            Vector3D(3, 3, 0),
        ],
    )
    other_scanner = UnderwaterScanner(
        scanner_id=1,
        visible_beacons_relative_coordinates=[
            Vector3D(-1, -1, 0),
            Vector3D(-5, 0, 0),
            Vector3D(-2, 0, 0),
        ],
    )
    pinpointed_scanner = reference_scanner.pinpoint(
        other_scanner, min_num_matching_beacons=3
    )
    assert pinpointed_scanner is None


def test_underwater_scanner_cannot_pinpoint_other_scanner_position_if_appropriate_number_of_beacons_align():
    reference_scanner = _reference_scanner(
        visible_beacons_relative_coordinates=[
            Vector3D(0, 2, 0),
            Vector3D(4, 1, 0),
            Vector3D(3, 3, 0),
        ],
    )
    other_scanner = UnderwaterScanner(
        scanner_id=1,
        visible_beacons_relative_coordinates=[
            Vector3D(-1, -1, 0),
            Vector3D(-5, 0, 0),
            Vector3D(-2, 1, 0),
        ],
    )
    pinpointed_scanner = reference_scanner.pinpoint(
        other_scanner, min_num_matching_beacons=3
    )
    assert pinpointed_scanner == PinpointedScanner(
        scanner_id=other_scanner.scanner_id,
        position=Vector3D(5, 2, 0),
        orientation=Orientation(x_prime=Vector3D(1, 0, 0), y_prime=Vector3D(0, 1, 0)),
        visible_beacons_relative_coordinates=other_scanner.visible_beacons_relative_coordinates,
    )


def test_underwater_scanner_cannot_pinpoint_other_scanner_orientation_if_appropriate_number_of_beacons_align():
    reference_scanner = _reference_scanner(
        visible_beacons_relative_coordinates=[
            Vector3D(404, -588, -901),
            Vector3D(528, -643, 409),
            Vector3D(-838, 591, 734),
            Vector3D(390, -675, -793),
            Vector3D(-537, -823, -458),
            Vector3D(-485, -357, 347),
            Vector3D(-345, -311, 381),
            Vector3D(-661, -816, -575),
            Vector3D(-876, 649, 763),
            Vector3D(-618, -824, -621),
            Vector3D(553, 345, -567),
            Vector3D(474, 580, 667),
            Vector3D(-447, -329, 318),
            Vector3D(-584, 868, -557),
            Vector3D(544, -627, -890),
            Vector3D(564, 392, -477),
            Vector3D(455, 729, 728),
            Vector3D(-892, 524, 684),
            Vector3D(-689, 845, -530),
            Vector3D(423, -701, 434),
            Vector3D(7, -33, -71),
            Vector3D(630, 319, -379),
            Vector3D(443, 580, 662),
            Vector3D(-789, 900, -551),
            Vector3D(459, -707, 401),
        ],
    )
    other_scanner = UnderwaterScanner(
        scanner_id=1,
        visible_beacons_relative_coordinates=[
            Vector3D(686, 422, 578),
            Vector3D(605, 423, 415),
            Vector3D(515, 917, -361),
            Vector3D(-336, 658, 858),
            Vector3D(95, 138, 22),
            Vector3D(-476, 619, 847),
            Vector3D(-340, -569, -846),
            Vector3D(567, -361, 727),
            Vector3D(-460, 603, -452),
            Vector3D(669, -402, 600),
            Vector3D(729, 430, 532),
            Vector3D(-500, -761, 534),
            Vector3D(-322, 571, 750),
            Vector3D(-466, -666, -811),
            Vector3D(-429, -592, 574),
            Vector3D(-355, 545, -477),
            Vector3D(703, -491, -529),
            Vector3D(-328, -685, 520),
            Vector3D(413, 935, -424),
            Vector3D(-391, 539, -444),
            Vector3D(586, -435, 557),
            Vector3D(-364, -763, -893),
            Vector3D(807, -499, -711),
            Vector3D(755, -354, -619),
            Vector3D(553, 889, -390),
        ],
    )
    pinpointed_scanner = reference_scanner.pinpoint(
        other_scanner, min_num_matching_beacons=12
    )
    assert pinpointed_scanner == PinpointedScanner(
        scanner_id=other_scanner.scanner_id,
        position=Vector3D(68, -1246, -43),
        orientation=Orientation(x_prime=Vector3D(-1, 0, 0), y_prime=Vector3D(0, 1, 0)),
        visible_beacons_relative_coordinates=other_scanner.visible_beacons_relative_coordinates,
    )


def test_all_underwater_scanners_in_a_list_are_pinpointed_by_finding_matching_beacons():
    scanners = [
        UnderwaterScanner(
            scanner_id=0,
            visible_beacons_relative_coordinates=(
                Vector3D(404, -588, -901),
                Vector3D(528, -643, 409),
                Vector3D(-838, 591, 734),
                Vector3D(390, -675, -793),
                Vector3D(-537, -823, -458),
                Vector3D(-485, -357, 347),
                Vector3D(-345, -311, 381),
                Vector3D(-661, -816, -575),
                Vector3D(-876, 649, 763),
                Vector3D(-618, -824, -621),
                Vector3D(553, 345, -567),
                Vector3D(474, 580, 667),
                Vector3D(-447, -329, 318),
                Vector3D(-584, 868, -557),
                Vector3D(544, -627, -890),
                Vector3D(564, 392, -477),
                Vector3D(455, 729, 728),
                Vector3D(-892, 524, 684),
                Vector3D(-689, 845, -530),
                Vector3D(423, -701, 434),
                Vector3D(7, -33, -71),
                Vector3D(630, 319, -379),
                Vector3D(443, 580, 662),
                Vector3D(-789, 900, -551),
                Vector3D(459, -707, 401),
            ),
        ),
        UnderwaterScanner(
            scanner_id=1,
            visible_beacons_relative_coordinates=(
                Vector3D(686, 422, 578),
                Vector3D(605, 423, 415),
                Vector3D(515, 917, -361),
                Vector3D(-336, 658, 858),
                Vector3D(95, 138, 22),
                Vector3D(-476, 619, 847),
                Vector3D(-340, -569, -846),
                Vector3D(567, -361, 727),
                Vector3D(-460, 603, -452),
                Vector3D(669, -402, 600),
                Vector3D(729, 430, 532),
                Vector3D(-500, -761, 534),
                Vector3D(-322, 571, 750),
                Vector3D(-466, -666, -811),
                Vector3D(-429, -592, 574),
                Vector3D(-355, 545, -477),
                Vector3D(703, -491, -529),
                Vector3D(-328, -685, 520),
                Vector3D(413, 935, -424),
                Vector3D(-391, 539, -444),
                Vector3D(586, -435, 557),
                Vector3D(-364, -763, -893),
                Vector3D(807, -499, -711),
                Vector3D(755, -354, -619),
                Vector3D(553, 889, -390),
            ),
        ),
        UnderwaterScanner(
            scanner_id=2,
            visible_beacons_relative_coordinates=(
                Vector3D(649, 640, 665),
                Vector3D(682, -795, 504),
                Vector3D(-784, 533, -524),
                Vector3D(-644, 584, -595),
                Vector3D(-588, -843, 648),
                Vector3D(-30, 6, 44),
                Vector3D(-674, 560, 763),
                Vector3D(500, 723, -460),
                Vector3D(609, 671, -379),
                Vector3D(-555, -800, 653),
                Vector3D(-675, -892, -343),
                Vector3D(697, -426, -610),
                Vector3D(578, 704, 681),
                Vector3D(493, 664, -388),
                Vector3D(-671, -858, 530),
                Vector3D(-667, 343, 800),
                Vector3D(571, -461, -707),
                Vector3D(-138, -166, 112),
                Vector3D(-889, 563, -600),
                Vector3D(646, -828, 498),
                Vector3D(640, 759, 510),
                Vector3D(-630, 509, 768),
                Vector3D(-681, -892, -333),
                Vector3D(673, -379, -804),
                Vector3D(-742, -814, -386),
                Vector3D(577, -820, 562),
            ),
        ),
        UnderwaterScanner(
            scanner_id=3,
            visible_beacons_relative_coordinates=(
                Vector3D(-589, 542, 597),
                Vector3D(605, -692, 669),
                Vector3D(-500, 565, -823),
                Vector3D(-660, 373, 557),
                Vector3D(-458, -679, -417),
                Vector3D(-488, 449, 543),
                Vector3D(-626, 468, -788),
                Vector3D(338, -750, -386),
                Vector3D(528, -832, -391),
                Vector3D(562, -778, 733),
                Vector3D(-938, -730, 414),
                Vector3D(543, 643, -506),
                Vector3D(-524, 371, -870),
                Vector3D(407, 773, 750),
                Vector3D(-104, 29, 83),
                Vector3D(378, -903, -323),
                Vector3D(-778, -728, 485),
                Vector3D(426, 699, 580),
                Vector3D(-438, -605, -362),
                Vector3D(-469, -447, -387),
                Vector3D(509, 732, 623),
                Vector3D(647, 635, -688),
                Vector3D(-868, -804, 481),
                Vector3D(614, -800, 639),
                Vector3D(595, 780, -596),
            ),
        ),
        UnderwaterScanner(
            scanner_id=4,
            visible_beacons_relative_coordinates=(
                Vector3D(727, 592, 562),
                Vector3D(-293, -554, 779),
                Vector3D(441, 611, -461),
                Vector3D(-714, 465, -776),
                Vector3D(-743, 427, -804),
                Vector3D(-660, -479, -426),
                Vector3D(832, -632, 460),
                Vector3D(927, -485, -438),
                Vector3D(408, 393, -506),
                Vector3D(466, 436, -512),
                Vector3D(110, 16, 151),
                Vector3D(-258, -428, 682),
                Vector3D(-393, 719, 612),
                Vector3D(-211, -452, 876),
                Vector3D(808, -476, -593),
                Vector3D(-575, 615, 604),
                Vector3D(-485, 667, 467),
                Vector3D(-680, 325, -822),
                Vector3D(-627, -443, -432),
                Vector3D(872, -547, -609),
                Vector3D(833, 512, 582),
                Vector3D(807, 604, 487),
                Vector3D(839, -516, 451),
                Vector3D(891, -625, 532),
                Vector3D(-652, -548, -490),
                Vector3D(30, -46, -14),
            ),
        ),
    ]
    pinpointed = pinpoint_scanners(scanners, min_num_matching_beacons=12)
    all_beacons = set()
    for scanner in pinpointed:
        all_beacons.update(scanner.visible_beacons_absolute_coordinates())
    assert len(all_beacons) == 79
