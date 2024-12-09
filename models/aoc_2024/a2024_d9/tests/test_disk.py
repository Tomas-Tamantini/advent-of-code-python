from ..logic import Disk, DiskFile


def test_disk_checksum_is_calculated_properly():
    files = {
        DiskFile(file_id=0, start_address=0, size=1),
        DiskFile(file_id=1, start_address=3, size=3),
        DiskFile(file_id=2, start_address=10, size=5),
    }
    disk = Disk(files)
    assert disk.compacted_checksum() == 60
