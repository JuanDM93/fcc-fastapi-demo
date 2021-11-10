import pytest
from app.models import Vote


@pytest.fixture
def test_vote(test_user, session, test_posts):
    vote = Vote(user_id=test_user['id'], post_id=test_posts[0].id)
    session.add(vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert response.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert response.status_code == 409


def test_vote_delete(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 0})
    assert response.status_code == 201


def test_vote_already_deleted(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 0})
    assert response.status_code == 404


def test_vote_no_post(authorized_client):
    response = authorized_client.post(
        "/vote/", json={"post_id": 1, "direction": 1})
    assert response.status_code == 404


def test_vote_unauthenticated(client):
    response = client.post(
        "/vote/", json={"post_id": 1, "direction": 1})
    assert response.status_code == 401
