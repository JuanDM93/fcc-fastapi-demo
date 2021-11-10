import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')
    map(lambda post: schemas.PostOut(**post), response.json())
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_get_all_posts_unauthorized(client):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_get_post_unauthorized(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_post_not_found(authorized_client):
    response = authorized_client.get('/posts/0')
    assert response.status_code == 404


def test_get_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    'title, content, published',
    [
        ('title1', 'content1', True),
        ('title2', 'content2', False),
        ('title3', 'content3', True),
    ]
)
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        '/posts/',
        json={'title': title, 'content': content, 'published': published})

    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user['id']


def test_create_post_default(authorized_client, test_user):
    response = authorized_client.post(
        '/posts/',
        json={'title': 'title1', 'content': 'content1'})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.published is True
    assert created_post.owner.id == test_user['id']


def test_create_unauthorized_post(client):
    response = client.post(
        '/posts/',
        json={'title': 'title1', 'content': 'content1'})
    assert response.status_code == 401


def test_delete_unauthorized_post(client, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204


def test_delete_not_found_post(authorized_client):
    response = authorized_client.delete('/posts/0')
    assert response.status_code == 404


def test_delete_other_post(authorized_client, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[1].id}')
    assert response.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        'title': 'title1',
        'content': 'content1',
        'id': test_posts[0].id
    }
    response = authorized_client.put(
        f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_post(authorized_client, test_posts):
    data = {
        'title': 'title1',
        'content': 'content1',
        'id': test_posts[1].id
    }
    response = authorized_client.put(
        f'/posts/{test_posts[1].id}', json=data)
    assert response.status_code == 403


def test_update_unauthorized_post(client, test_posts):
    data = {
        'title': 'title1',
        'content': 'content1',
        'id': test_posts[0].id
    }
    response = client.put(
        f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 401


def test_update_not_found_post(authorized_client):
    data = {
        'title': 'title1',
        'content': 'content1',
        'id': 0
    }
    response = authorized_client.put(
        f'/posts/{data["id"]}', json=data)
    assert response.status_code == 404
