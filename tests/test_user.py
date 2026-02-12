def test_register_success(client):
    response = client.post("/add", json={
        "first_name": "Marie",
        "last_name": "Curie",
        "email": "marie@example.com",
        "password": "radioactive42",
        "date_of_birth": "1867-11-07"
    })
    assert response.status_code == 201
    assert "user_id" in response.json


def test_register_duplicate_email(client):
    # Premier enregistrement
    client.post("/add", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "duplicate@example.com",
        "password": "pass123",
        "date_of_birth": "1990-01-01"
    })
    # Deuxième → devrait échouer (car email unique)
    response = client.post("/add", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "duplicate@example.com",
        "password": "pass456",
        "date_of_birth": "1992-03-03"
    })
    assert response.status_code == 500   # ← ton code actuel plante sur IntegrityError
    # Note : idéalement tu devrais catcher l'erreur et renvoyer 409 ou 400


def test_update_own_user(client, registered_user):
    response = client.put(
        f"/update/{registered_user['id']}",
        json={"first_name": "UpdatedName"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 200
    assert "UpdatedName" in response.json["user"]  # selon ce que retourne update_user


def test_update_other_user_forbidden(client, registered_user):
    # On suppose qu'un autre user existe déjà (créé dans registered_user fixture)
    other_user_id = 999  # mauvais ID
    response = client.put(
        f"/update/{other_user_id}",
        json={"first_name": "Hacked"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 403