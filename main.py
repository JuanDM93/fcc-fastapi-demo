from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return None


my_posts = [
    {
        'title': "Example Post 1",
        'content': "Just a test 1",
        'id': 1,
    },
    {
        'title': "Example Post 2",
        'content': "Just a test 2",
        'id': 2,
    },
]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    post['id'] = len(my_posts) + 1
    my_posts.append(post)
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id: {id} not found"
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id: {id} does not exists"
        )
    my_posts.pop(index)
    return {Response(status_code=status.HTTP_204_NO_CONTENT)}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id: {id} does not exists"
        )
    my_post = post.dict()
    my_post['id'] = id
    my_posts[index] = my_post
    return {"data": my_post}
