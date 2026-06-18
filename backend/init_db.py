from app.database.session import engine
from app.models.user import User
from app.models.approval_request import ApprovalRequest
from app.models.review_action import ReviewAction

def create_tables():
    print("⏳ Creating database tables...")
    # Yeh command database mein saari missing tables generate kar degi
    User.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    create_tables()