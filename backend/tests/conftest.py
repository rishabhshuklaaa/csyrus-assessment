import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Core FastAPI application instance import
from main import app 

from app.database.session import get_db

from app.models.user import User

# Use SQLite In-Memory database for fast, completely isolated testing cycles 
# This completely decouples testing from the production/local PostgreSQL configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh database schema instance for every isolated test case 
    using declarative model metadata registry tables.
    """
    
    User.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        User.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Overrides the core application database injection dependency hooks 
    and provisions a functional FastAPI TestClient instance.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
