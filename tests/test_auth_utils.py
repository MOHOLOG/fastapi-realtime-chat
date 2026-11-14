import jwt
import pytest

from auth import utils


def test_hash_password_returns_hashed_value():
    hashed = utils.hash_password("supersecret123")

    assert isinstance(hashed, str)
    assert hashed != "supersecret123"


def test_verify_password_with_correct_password():
    hashed = utils.hash_password("supersecret123")

    assert utils.verify_password("supersecret123".encode(), hashed.encode()) is True


def test_verify_password_with_wrong_password():
    hashed = utils.hash_password("supersecret123")

    assert utils.verify_password("wrongpassword".encode(), hashed.encode()) is False


def test_encode_jwt_returns_token():
    token = utils.encode_jwt({"username": "alice"})

    assert isinstance(token, str)
    assert token.count(".") == 2


def test_decode_jwt_roundtrip():
    token = utils.encode_jwt({"username": "alice", "email": "alice@example.com"})

    payload = utils.decode_jwt(token)

    assert payload["username"] == "alice"
    assert payload["email"] == "alice@example.com"
    assert "exp" in payload
    assert "iat" in payload


def test_decode_jwt_with_invalid_token_raises():
    with pytest.raises(jwt.PyJWTError):
        utils.decode_jwt("this.is.not-a-real-token")
