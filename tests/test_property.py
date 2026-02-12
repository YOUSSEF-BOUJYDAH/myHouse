def test_add_property_success(client, registered_user):
    response = client.post(
        "/add",
        json={
            "name": "Appartement Lyon",
            "description": "Beau T2",
            "type": "Appartement",
            "city": "Lyon"
        },
        headers=registered_user["headers"]
    )
    assert response.status_code == 201
    assert "property_id" in response.json


def test_add_property_unauthenticated(client):
    response = client.post("/add", json={
        "name": "No auth",
        "type": "Maison",
        "city": "Paris"
    })
    # Ton code actuel renvoie 500 (car get_jwt_identity() plante sans token)
    # → 401 serait mieux, mais pour l'instant on teste le comportement existant
    assert response.status_code == 500   # à améliorer dans l'app


def test_update_own_property(client, registered_user):
    # Créer d'abord
    create_resp = client.post(
        "/add",
        json={
            "name": "To Update",
            "type": "Studio",
            "city": "Marseille"
        },
        headers=registered_user["headers"]
    )
    prop_id = create_resp.json["property_id"]

    # Update
    update_resp = client.put(
        f"/update/{prop_id}",
        json={"name": "Updated Studio"},
        headers=registered_user["headers"]
    )
    assert update_resp.status_code == 200


def test_update_not_owner_should_fail(client, registered_user):
    # On crée une property avec l'utilisateur test
    create_resp = client.post(
        "/add",
        json={"name": "Protected", "type": "Villa", "city": "Nice"},
        headers=registered_user["headers"]
    )
    prop_id = create_resp.json["property_id"]

    # Créer un deuxième utilisateur
    client.post("/add", json={
        "first_name": "Hacker",
        "last_name": "Test",
        "email": "hacker@example.com",
        "password": "hack123",
        "date_of_birth": "2000-01-01"
    })
    hacker_login = client.post("/login", json={
        "email": "hacker@example.com",
        "password": "hack123"
    })
    hacker_token = hacker_login.json["access_token"]
    hacker_headers = {"Authorization": f"Bearer {hacker_token}"}

    # Tentative de modification → devrait échouer
    response = client.put(
        f"/update/{prop_id}",
        json={"name": "Hacked Property"},
        headers=hacker_headers
    )
    assert response.status_code == 403
    assert "not the owner" in response.json["msg"]