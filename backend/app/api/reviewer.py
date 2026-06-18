from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.approval_request import ApprovalRequestResponse
from app.schemas.review_action import ReviewActionCreate
from app.services.reviewer_service import reviewer_service

router = APIRouter()

@router.get("/requests", response_model=List[ApprovalRequestResponse])
def get_assigned_requests(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """View requests assigned to the logged-in reviewer."""
    return reviewer_service.get_assigned_requests(db=db, reviewer_id=current_user.id, skip=skip, limit=limit)

@router.post("/requests/{id}/approve", response_model=ApprovalRequestResponse)
def approve_request(
    id: UUID, 
    review_in: ReviewActionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Approve a pending request."""
    return reviewer_service.process_request(db=db, request_id=id, reviewer_id=current_user.id, action="APPROVED", schema=review_in)

@router.post("/requests/{id}/reject", response_model=ApprovalRequestResponse)
def reject_request(
    id: UUID, 
    review_in: ReviewActionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Reject a pending request."""
    return reviewer_service.process_request(db=db, request_id=id, reviewer_id=current_user.id, action="REJECTED", schema=review_in)