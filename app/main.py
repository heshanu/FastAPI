from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import PostCreate, Post
from .dao.postDao import PostDAO

app = FastAPI()

@app.post("/post", response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post_dao = PostDAO(db)
    return post_dao.create_post(post)

@app.get("/posts", response_model=list[Post])
def get_all_posts(db: Session = Depends(get_db)):
    post_dao = PostDAO(db)
    return post_dao.get_all_posts()

@app.get("/post/{post_id}", response_model=Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post_dao = PostDAO(db)
    post = post_dao.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_dao = PostDAO(db)
    post_dao.delete_post(post_id)
    return {"detail": "Post deleted"}
