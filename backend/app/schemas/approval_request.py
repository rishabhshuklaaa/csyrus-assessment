from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class ApprovalRequestBase(BaseModel):
    title: str
    description: str
    priority: str  # LOW, MEDIUM, HIGH
    reviewer_id: UUID

class ApprovalRequestCreate(ApprovalRequestBase):
    pass

class ApprovalRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    reviewer_id: Optional[UUID] = None

class ApprovalRequestResponse(ApprovalRequestBase):
    id: UUID
    status: str
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)