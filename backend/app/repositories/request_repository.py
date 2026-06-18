from sqlalchemy.orm import Session
from uuid import UUID
from app.models.approval_request import ApprovalRequest

class RequestRepository:
    def create(self, db: Session, obj_in: dict) -> ApprovalRequest:
        db_obj = ApprovalRequest(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: UUID) -> ApprovalRequest | None:
        return db.query(ApprovalRequest).filter(ApprovalRequest.id == id).first()

    def get_multi_by_user(self, db: Session, user_id: UUID, skip: int = 0, limit: int = 10):
        return db.query(ApprovalRequest).filter(ApprovalRequest.created_by == user_id).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: ApprovalRequest, obj_in: dict) -> ApprovalRequest:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ApprovalRequest) -> None:
        db.delete(db_obj)
        db.commit()

request_repo = RequestRepository()