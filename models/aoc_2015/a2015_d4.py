from hashlib import md5


def md5_hash(message: str) -> str:
    return md5(message.encode()).hexdigest()


def mine_advent_coins(secret_key: str, num_leading_zeros: int) -> int:
    number = 0
    starting_zeros = "0" * num_leading_zeros
    while True:
        number += 1
        message = secret_key + str(number)
        hashed_message = md5_hash(message)
        if hashed_message.startswith(starting_zeros):
            return number
