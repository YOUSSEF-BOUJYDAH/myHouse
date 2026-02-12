def test_login_success(client, registered_user):
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_wrong_password(client, registered_user):
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Bad email or password" in response.json["msg"]


def test_login_non_existing_user(client):
    response = client.post("/login", json={
        "email": "unknown@example.com",
        "password": "whatever"
    })
    assert response.status_code == 401