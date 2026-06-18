from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.approval_request import ApprovalRequestCreate, ApprovalRequestUpdate, ApprovalRequestResponse
from app.services.request_service import request_service

router = APIRouter()

@router.post("/", response_model=ApprovalRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(
    request_in: ApprovalRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new approval request."""
    return request_service.create_request(db=db, schema=request_in, user_id=current_user.id)

@router.get("/", response_model=List[ApprovalRequestResponse])
def read_requests(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all requests created by the current user (Paginated)."""
    return request_service.get_requests_for_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{id}", response_model=ApprovalRequestResponse)
def read_request(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a specific request."""
    return request_service.get_single_request(db=db, request_id=id, user_id=current_user.id)

@router.put("/{id}", response_model=ApprovalRequestResponse)
def update_request(
    id: UUID,
    request_in: ApprovalRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a specific request (Only if PENDING)."""
    return request_service.update_request(db=db, request_id=id, schema=request_in, user_id=current_user.id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_request(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific request (Only if PENDING)."""
    request_service.delete_request(db=db, request_id=id, user_id=current_user.id)