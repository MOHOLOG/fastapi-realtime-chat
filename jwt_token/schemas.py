from pydantic import BaseModel

class TokenResponse(BaseModel):
    secret_token: str
    token_type: str