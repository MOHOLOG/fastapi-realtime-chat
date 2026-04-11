from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent

class Auth_JWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    expire_time_minutes: int = 30