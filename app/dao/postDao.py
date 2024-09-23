from sqlalchemy.orm import Session
from ..models import Post
from ..schemas import PostCreate

class PostDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all_posts(self):
        return self.db.query(Post).all()

    def get_post_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def create_post(self, post: PostCreate):
        new_post = Post(title=post.title, content=post.content)
        self.db.add(new_post)
        self.db.commit()
        self.db.refresh(new_post)
        return new_post

    def delete_post(self, post_id: int):
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post:
            self.db.delete(post)
            self.db.commit()
