import string
import random

ALPHABET = string.ascii_letters + string.digits
BASE = len(ALPHABET)

def encode_id(num: int) -> str:
    """Encode an integer ID into a Base62 string."""
    if num == 0:
        return ALPHABET[0]
    arr = []
    base = len(ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    arr.reverse()
    return ''.join(arr)

def decode_id(short_str: str) -> int:
    """Decode a Base62 string back to an integer ID."""
    base = len(ALPHABET)
    num = 0
    for char in short_str:
        num = num * base + ALPHABET.index(char)
    return num

def generate_random_short_id(length: int = 7) -> str:
    """Generate a random Base62 string of a specific length."""
    return ''.join(random.choices(ALPHABET, k=length))
