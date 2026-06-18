from sqlalchemy.orm import Session
from app.models.review_action import ReviewAction

class ReviewRepository:
    def create(self, db: Session, obj_in: dict) -> ReviewAction:
        db_obj = ReviewAction(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

review_repo = ReviewRepository()