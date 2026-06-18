import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class ReviewAction(Base):
    __tablename__ = "review_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("approval_requests.id"), nullable=False)
    action = Column(String, nullable=False) # APPROVED, REJECTED
    comments = Column(Text, nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    request = relationship("ApprovalRequest")
    reviewer = relationship("User", foreign_keys=[reviewed_by])