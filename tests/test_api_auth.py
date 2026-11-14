REGISTER_PAYLOAD = {
    "username": "alice",
    "email": "alice@example.com",
    "password": "password123",
}


async def test_register_user_success(client):
    response = await client.post("/register", json=REGISTER_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"


async def test_register_duplicate_username_returns_400(client):
    await client.post("/register", json=REGISTER_PAYLOAD)

    response = await client.post("/register", json=REGISTER_PAYLOAD)

    assert response.status_code == 400


async def test_register_invalid_email_returns_422(client):
    payload = {**REGISTER_PAYLOAD, "email": "not-an-email"}

    response = await client.post("/register", json=payload)

    assert response.status_code == 422


async def test_register_short_password_returns_422(client):
    payload = {**REGISTER_PAYLOAD, "password": "short"}

    response = await client.post("/register", json=payload)

    assert response.status_code == 422


async def test_login_success_returns_token(client):
    await client.post("/register", json=REGISTER_PAYLOAD)

    response = await client.post(
        "/login",
        json={"email": "alice@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "secret_token" in body
    assert body["token_type"] == "bearer"


async def test_login_wrong_password_returns_404(client):
    await client.post("/register", json=REGISTER_PAYLOAD)

    response = await client.post(
        "/login",
        json={"email": "alice@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 404


async def test_login_unknown_email_returns_404(client):
    response = await client.post(
        "/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )

    assert response.status_code == 404
