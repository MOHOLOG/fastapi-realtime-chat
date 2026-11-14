import pytest
from pydantic import ValidationError

from message.schemas import MessageCreate
from user.schemas import UserCreate


def test_user_create_accepts_valid_data():
    user = UserCreate(
        username="alice",
        email="alice@example.com",
        password="password123",
    )

    assert user.username == "alice"
    assert user.email == "alice@example.com"


def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="alice@example.com", password="short")


def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(username="alice", email="not-an-email", password="password123")


def test_message_create_accepts_valid_text():
    message = MessageCreate(text="hello world")

    assert message.text == "hello world"


def test_message_create_rejects_empty_text():
    with pytest.raises(ValidationError):
        MessageCreate(text="")
