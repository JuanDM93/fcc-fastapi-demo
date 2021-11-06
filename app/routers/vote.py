from fastapi.param_functions import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status

from ..db import get_db
from .. import schemas, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found")

    v_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id
    )
    found = v_query.first()
    if vote.direction == 1:
        if found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted for this post"
            )
        n_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(n_vote)
        db.commit()
        return {"message": "Vote created"}
    else:
        if not found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        v_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted"}
