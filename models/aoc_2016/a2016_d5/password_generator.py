from math import ceil
from hashlib import md5
from typing import Iterator, Optional
from models.common.io import ProgressBar


class PasswordGenerator:
    def __init__(self, door_id: str, num_zeroes: int, password_length: int):
        self._door_id = door_id
        self._num_zeroes = num_zeroes
        self._password_length = password_length
        self._password_left_to_right: list[chr] = []
        self._password_one_position_at_a_time: list[chr] = ["*"] * password_length

    def indices_whose_hash_start_with_zeroes(self) -> Iterator[tuple[int, str]]:
        index = 0
        leading_zeroes = "0" * self._num_zeroes
        while True:
            hashed = md5((self._door_id + str(index)).encode("utf-8")).hexdigest()
            if hashed.startswith(leading_zeroes):
                yield index, hashed
            index += 1

    @property
    def password_left_to_right(self) -> str:
        return "".join(self._password_left_to_right)

    @property
    def password_one_position_at_a_time(self) -> str:
        return "".join(self._password_one_position_at_a_time)

    def _passwords_are_complete(self) -> bool:
        return "*" not in self._password_one_position_at_a_time

    def _update_password_left_to_right(self, next_char: chr) -> None:
        if len(self._password_left_to_right) < self._password_length:
            self._password_left_to_right.append(next_char)

    def _update_password_one_position_at_a_time(
        self, next_char: chr, position: chr
    ) -> None:
        try:
            position = int(position)
        except ValueError:
            return
        if (
            0 <= position < self._password_length
            and self._password_one_position_at_a_time[position] == "*"
        ):
            self._password_one_position_at_a_time[position] = next_char

    def generate_passwords(self, progress_bar: Optional[ProgressBar] = None) -> None:
        count = 0
        expected_count = ceil(
            1.5
            * sum(
                self._password_length / i for i in range(1, self._password_length + 1)
            )
        )
        for _, hashed in self.indices_whose_hash_start_with_zeroes():
            if progress_bar:
                progress_bar.update(count, expected_count)
                count += 1
            if self._passwords_are_complete():
                break
            self._update_password_left_to_right(hashed[self._num_zeroes])
            self._update_password_one_position_at_a_time(
                hashed[self._num_zeroes + 1], hashed[self._num_zeroes]
            )
