from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Truncate to max 72 bytes
    max_bytes = 72
    encoded = password.encode("utf-8")[:max_bytes]  # truncate if longer
    truncated = encoded.decode("utf-8", "ignore")   # decode back
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    max_bytes = 72
    encoded = plain_password.encode("utf-8")[:max_bytes]
    truncated = encoded.decode("utf-8", "ignore")
    return pwd_context.verify(truncated, hashed_password)
