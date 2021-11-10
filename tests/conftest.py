import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.config import settings
from app.db import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{db}_test'.format(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    db=settings.DB_NAME
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test_user@mail.com", "password": "test_password"}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def test_other_user(client):
    user_data = {"email": "other_user@mail.com", "password": "other_password"}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(session, test_user, test_other_user):
    post_data = [
        {
            "title": "Test Post 1", "content": "Test Content 1",
            "owner_id": test_user['id'],
        },
        {
            "title": "Test Post 2", "content": "Test Content 2",
            "owner_id": test_other_user['id'],
        },
        {
            "title": "Test Post 3", "content": "Test Content 3",
            "owner_id": test_user['id'],
        },
    ]
    post_map = map(lambda post: models.Post(**post), post_data)
    session.add_all(list(post_map))
    session.commit()
    posts = session.query(models.Post).all()
    return posts
