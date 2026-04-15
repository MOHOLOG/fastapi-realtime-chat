from datetime import datetime, timedelta
from auth.schema_jwt import Auth_JWT
import bcrypt   
import jwt
from zoneinfo import ZoneInfo

zone = ZoneInfo("Europe/Moscow")

settings = Auth_JWT()

def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    return hashed_password

def verify_password(passed_password: bytes, current_password: bytes):
    return bcrypt.checkpw(passed_password, current_password)

def encode_jwt(
        payload: dict,
        private_key: str = settings.private_key_path.read_text(),
        algorithm: str = settings.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.expire_time_minutes
    ):

    payload_copy = payload.copy()
    now = datetime.now(zone)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    payload_copy.update({"exp": expire, "iat": now})

    encoded = jwt.encode(payload=payload_copy, key=private_key, algorithm=algorithm)

    return encoded

def decode_jwt(
        token: str,
        public_key: str = settings.public_key_path.read_text(),
        algorithm: str = settings.algorithm
    ):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=algorithm)

    return decoded