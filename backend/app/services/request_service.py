from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.schemas.approval_request import ApprovalRequestCreate, ApprovalRequestUpdate
from app.repositories.request_repository import request_repo

class RequestService:
    def create_request(self, db: Session, schema: ApprovalRequestCreate, user_id: UUID):
        data = schema.model_dump()
        data["created_by"] = user_id
        data["status"] = "PENDING"
        return request_repo.create(db=db, obj_in=data)

    def get_requests_for_user(self, db: Session, user_id: UUID, skip: int, limit: int):
        return request_repo.get_multi_by_user(db=db, user_id=user_id, skip=skip, limit=limit)

    def get_single_request(self, db: Session, request_id: UUID, user_id: UUID):
        request = request_repo.get(db=db, id=request_id)
        if not request or request.created_by != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return request

    def update_request(self, db: Session, request_id: UUID, schema: ApprovalRequestUpdate, user_id: UUID):
        request = self.get_single_request(db=db, request_id=request_id, user_id=user_id)
        
        # Core Business Logic: Can only edit PENDING requests
        if request.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Cannot edit a request that is already Approved or Rejected"
            )
            
        update_data = schema.model_dump(exclude_unset=True)
        return request_repo.update(db=db, db_obj=request, obj_in=update_data)

    def delete_request(self, db: Session, request_id: UUID, user_id: UUID):
        request = self.get_single_request(db=db, request_id=request_id, user_id=user_id)
        
        # Core Business Logic: Can only delete PENDING requests
        if request.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Cannot delete a request that is already Approved or Rejected"
            )
            
        request_repo.delete(db=db, db_obj=request)

request_service = RequestService()