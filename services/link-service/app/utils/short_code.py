import secrets
import string

DEFAULT_ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(length))
