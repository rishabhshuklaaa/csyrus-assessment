from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import verify_token
from app.models.user import User

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # We will look for the token in cookies, as it's more secure for SPAs
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to Authorization header if testing via Postman
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    payload = verify_token(token)
    if not payload:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
         
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    return user