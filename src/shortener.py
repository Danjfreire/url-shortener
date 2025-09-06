import secrets
import random
from constants import ALPHABET, MAX_CODE_LEN, MIN_CODE_LEN, MAX_TRIES

def generate_random_code(length: int | None = None) -> str | None:
    if length is None:
        length = random.randrange(MIN_CODE_LEN, MAX_CODE_LEN)

    return ''.join(secrets.choice(ALPHABET) for i in range(length))



