from hashlib import md5


def generate_password(door_id: str):
    password = ""
    index = 0
    while len(password) < 8:
        hashed = md5((door_id + str(index)).encode("utf-8")).hexdigest()
        if hashed.startswith("00000"):
            password += hashed[5]
        index += 1
    return password
