import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.config import settings
from app.models.user import User
from app.core.security import create_access_token
from app.api.deps import get_current_user

router = APIRouter()

# Define admin emails for Role-Based Access Control (RBAC)
ADMIN_EMAILS = ["rishabhshuklaitm786@gmail.com", "admin@company.com"]

@router.get("/google/login")
def login_google():
    """Redirects to the Google OAuth consent screen."""
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline"
    )
    return RedirectResponse(url=auth_url)

@router.get("/google/callback")
def auth_google(code: str, db: Session = Depends(get_db)):
    """Handles Google OAuth callback, provisions users with roles, and issues JWT."""
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    # Exchange auth code for access token
    with httpx.Client() as client:
        response = client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get token from Google")
        
        access_token = response.json().get("access_token")
        
        # Fetch user profile from Google
        user_info_resp = client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if user_info_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
            
        user_data = user_info_resp.json()

    # Database logic for user creation/lookup
    email = user_data.get("email")
    google_id = user_data.get("id")
    name = user_data.get("name")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Assign Reviewer role if email is in ADMIN_EMAILS, else default to Requester
        assigned_role = "Reviewer" if email in ADMIN_EMAILS else "Requester"
        
        user = User(email=email, google_id=google_id, name=name, role=assigned_role)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate internal JWT
    jwt_token = create_access_token(data={"sub": str(user.id)})
    
    # Set HttpOnly cookie and redirect to frontend
    redirect_response = RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard")
    redirect_response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        max_age=86400, # 24 hours
        samesite="lax",
        secure=False # Set True in production (HTTPS)
    )
    
    return redirect_response

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the profile of the currently authenticated user."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

@router.get("/reviewers", summary="Get list of available reviewers")
def get_available_reviewers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Returns a list of ONLY Reviewers for the assignment dropdown."""
    # MAGIC FIX: Ab hum 'all()' ki jagah filter laga rahe hain taaki sirf Admins dikhein
    reviewers = db.query(User).filter(User.role == "Reviewer").all()
    return [{"id": str(r.id), "name": r.name} for r in reviewers]

@router.post("/logout")
def logout_user(response: Response):
    """Clears the authentication cookie to log the user out."""
    response.delete_cookie(
        key="access_token", 
        path="/", 
        httponly=True, 
        samesite="lax"
    )
    return {"message": "Logged out successfully"}