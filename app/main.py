from fastapi import FastAPI

from .db import engine
from .routers import auth, user, post
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
