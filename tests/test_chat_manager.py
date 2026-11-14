from datetime import datetime
from typing import cast

from fastapi import WebSocket

from chat.manager import ConnectionManager
from message.schemas import MessageResponse
from user.schemas import UserResponse


class FakeWebSocket:
    def __init__(self):
        self.accepted = False
        self.sent = []

    async def accept(self):
        self.accepted = True

    async def send_json(self, data):
        self.sent.append(data)


def as_websocket(fake: FakeWebSocket) -> WebSocket:
    return cast(WebSocket, fake)


def make_message():
    return MessageResponse(
        id=1,
        text="hello",
        user=UserResponse(
            id=1,
            username="alice",
            email="alice@example.com",
            created_at=datetime.now(),
        ),
        created_at=datetime.now(),
    )


async def test_connect_accepts_and_registers_user():
    manager = ConnectionManager()
    websocket = FakeWebSocket()

    await manager.connect(username="alice", websocket=as_websocket(websocket))

    assert websocket.accepted is True
    assert "alice" in manager.active_connections


async def test_disconnect_removes_user():
    manager = ConnectionManager()
    await manager.connect(username="alice", websocket=as_websocket(FakeWebSocket()))

    manager.disconnect(username="alice")

    assert "alice" not in manager.active_connections


async def test_is_rate_limited_returns_false_for_unknown_user():
    manager = ConnectionManager()

    assert await manager.is_rate_limited("ghost") is False


async def test_first_five_messages_are_allowed():
    manager = ConnectionManager()
    await manager.connect(username="alice", websocket=as_websocket(FakeWebSocket()))

    for _ in range(5):
        assert await manager.is_rate_limited("alice") is False


async def test_sixth_message_is_rate_limited():
    manager = ConnectionManager()
    await manager.connect(username="alice", websocket=as_websocket(FakeWebSocket()))

    for _ in range(5):
        await manager.is_rate_limited("alice")

    assert await manager.is_rate_limited("alice") is True


async def test_broadcast_skips_the_sender():
    manager = ConnectionManager()
    sender = FakeWebSocket()
    other = FakeWebSocket()
    await manager.connect(username="alice", websocket=as_websocket(sender))
    await manager.connect(username="bob", websocket=as_websocket(other))

    await manager.broadcast(username="alice", message=make_message())

    assert sender.sent == []
    assert len(other.sent) == 1
    assert other.sent[0]["text"] == "hello"
