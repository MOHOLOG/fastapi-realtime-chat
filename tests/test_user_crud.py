import pytest_asyncio

from user import crud
from user.schemas import UserCreate


@pytest_asyncio.fixture
async def created_user(db_session):
    user = await crud.create_user(
        user=UserCreate(
            username="alice",
            email="alice@example.com",
            password="password123",
        ),
        db=db_session,
    )
    return user


async def test_create_user(db_session):
    user = await crud.create_user(
        user=UserCreate(
            username="bob",
            email="bob@example.com",
            password="password123",
        ),
        db=db_session,
    )

    assert user.id is not None
    assert user.username == "bob"
    assert user.email == "bob@example.com"


async def test_create_user_hashes_password(db_session):
    user = await crud.create_user(
        user=UserCreate(
            username="bob",
            email="bob@example.com",
            password="password123",
        ),
        db=db_session,
    )

    assert user.hashed_password != "password123"


async def test_get_user_by_username(db_session, created_user):
    found = await crud.get_user_by_username(username="alice", db=db_session)

    assert found is not None
    assert found.id == created_user.id


async def test_get_user_by_username_not_found(db_session):
    found = await crud.get_user_by_username(username="nobody", db=db_session)

    assert found is None


async def test_get_user_by_email(db_session, created_user):
    found = await crud.get_user_by_email(email="alice@example.com", db=db_session)

    assert found is not None
    assert found.id == created_user.id


async def test_get_user_by_email_not_found(db_session):
    found = await crud.get_user_by_email(email="nobody@example.com", db=db_session)

    assert found is None
