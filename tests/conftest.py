import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture(scope="module")
def app():
    """Application Flask en mode test avec base SQLite en mémoire"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-jwt-secret-for-unit-tests-only",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture
def registered_user(client):
    """Crée un utilisateur et retourne son ID + token"""
    register_resp = client.post("/add", json={   # ton endpoint est /add pour register
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "testpass123",
        "date_of_birth": "1995-05-15"
    })
    assert register_resp.status_code == 201

    login_resp = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json["access_token"]

    user = User.query.filter_by(email="testuser@example.com").first()
    return {
        "id": user.id,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }