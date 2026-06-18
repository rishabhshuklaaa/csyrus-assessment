from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.models.approval_request import ApprovalRequest
from app.schemas.review_action import ReviewActionCreate
from app.repositories.review_repository import review_repo
from app.repositories.request_repository import request_repo

class ReviewerService:
    def get_assigned_requests(self, db: Session, reviewer_id: UUID, skip: int, limit: int):
        """Fetches requests where the current user is assigned as the reviewer."""
        return db.query(ApprovalRequest).filter(ApprovalRequest.reviewer_id == reviewer_id).offset(skip).limit(limit).all()
        
    def process_request(self, db: Session, request_id: UUID, reviewer_id: UUID, action: str, schema: ReviewActionCreate):
        """Approves or Rejects a request securely."""
        request = request_repo.get(db=db, id=request_id)
        
        # Validation 1: Request exists?
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
            
        # Validation 2: Is this user the assigned reviewer?
        if request.reviewer_id != reviewer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to review this request")
            
        # Validation 3: Is the request still PENDING? (Prevents double approval)
        if request.status != "PENDING":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Request is already {request.status}")
            
        # Update Request Status
        request.status = action
        db.commit()
        
        # Log the Review Action
        action_data = {
            "request_id": request.id,
            "action": action,
            "comments": schema.comments,
            "reviewed_by": reviewer_id
        }
        review_repo.create(db=db, obj_in=action_data)
        
        # Refresh and return updated request
        db.refresh(request)
        return request

reviewer_service = ReviewerService()