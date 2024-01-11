from models.aoc_2016 import EncryptedRoom


def test_room_is_real_if_checksum_is_valid():
    assert EncryptedRoom(
        room_name="aaaaa-bbb-z-y-x", sector_id=123, checksum="abxyz"
    ).is_real()

    assert EncryptedRoom(
        room_name="a-b-c-d-e-f-g-h", sector_id=987, checksum="abcde"
    ).is_real()

    assert EncryptedRoom(
        room_name="not-a-real-room", sector_id=404, checksum="oarel"
    ).is_real()


def test_room_is_not_real_if_checksum_is_invalid():
    assert not EncryptedRoom(
        room_name="totally-real-room", sector_id=200, checksum="decoy"
    ).is_real()


def test_room_name_can_be_decrypted_by_shifting_letters():
    assert (
        EncryptedRoom(
            room_name="qzmt-zixmtkozy-ivhz", sector_id=343, checksum="zimth"
        ).decrypt_name()
        == "very encrypted name"
    )
