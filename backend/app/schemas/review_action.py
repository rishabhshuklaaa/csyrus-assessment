from pydantic import BaseModel
from typing import Optional

class ReviewActionCreate(BaseModel):
    comments: Optional[str] = None