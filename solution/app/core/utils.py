import hashlib

def hash_sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()