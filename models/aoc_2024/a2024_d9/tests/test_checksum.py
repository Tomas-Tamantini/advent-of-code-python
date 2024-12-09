import pytest

from ..logic import DiskFile, fragmented_checksum, integral_checksum


def _example_a() -> set[DiskFile]:
    return {
        DiskFile(file_id=0, start_address=0, size=1),
        DiskFile(file_id=1, start_address=3, size=3),
        DiskFile(file_id=2, start_address=10, size=5),
    }


def _example_b() -> set[DiskFile]:
    return {
        DiskFile(file_id=0, start_address=0, size=2),
        DiskFile(file_id=1, start_address=5, size=3),
        DiskFile(file_id=2, start_address=11, size=1),
        DiskFile(file_id=3, start_address=15, size=3),
        DiskFile(file_id=4, start_address=19, size=2),
        DiskFile(file_id=5, start_address=22, size=4),
        DiskFile(file_id=6, start_address=27, size=4),
        DiskFile(file_id=7, start_address=32, size=3),
        DiskFile(file_id=8, start_address=36, size=4),
        DiskFile(file_id=9, start_address=40, size=2),
    }


@pytest.mark.parametrize(
    ("files", "expected_checksum"), [(_example_a(), 60), (_example_b(), 1928)]
)
def test_fragmented_checksum_is_calculated_properly(files, expected_checksum):
    assert expected_checksum == fragmented_checksum(files)


@pytest.mark.parametrize(
    ("files", "expected_checksum"), [(_example_a(), 132), (_example_b(), 2858)]
)
def test_integral_checksum_is_calculated_properly(files, expected_checksum):
    assert expected_checksum == integral_checksum(files)
