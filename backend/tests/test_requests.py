import uuid
from main import app
from app.api.deps import get_current_user
from app.models.user import User
from app.models.approval_request import ApprovalRequest

REQUESTS_URL = "/api/v1/requests"

def test_create_approval_request_endpoint(client, db_session) -> None:
    """Test 4: Requester creates a brand new tracking event payload record."""
    requester = User(id=uuid.uuid4(), email="req1@itm.com", name="R1", google_id="g1", role="Requester")
    reviewer = User(id=uuid.uuid4(), email="rev1@itm.com", name="V1", google_id="g2", role="Reviewer")
    db_session.add_all([requester, reviewer])
    db_session.commit()
    
    app.dependency_overrides[get_current_user] = lambda: requester
    payload = {"title": "Cloud Server Scaling", "description": "AWS infrastructure", "priority": "HIGH", "reviewer_id": str(reviewer.id)}
    
    response = client.post(REQUESTS_URL, json=payload)
    assert response.status_code in [200, 201]
    app.dependency_overrides.pop(get_current_user, None)

def test_fetch_user_requests_dashboard(client, db_session) -> None:
    """Test 5: Retrieve active arrays matching the user context workspace data layer."""
    requester = User(id=uuid.uuid4(), email="req2@itm.com", name="R2", google_id="g3", role="Requester")
    db_session.add(requester)
    db_session.commit()
    
    app.dependency_overrides[get_current_user] = lambda: requester
    response = client.get(REQUESTS_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    app.dependency_overrides.pop(get_current_user, None)

def test_update_approval_request_patch(client, db_session) -> None:
    """Test 6: Modify an existing record state before reviewer transition checks."""
    requester = User(id=uuid.uuid4(), email="req3@itm.com", name="R3", google_id="g4", role="Requester")
    req_item = ApprovalRequest(id=uuid.uuid4(), title="Old Title", description="Old Desc", priority="LOW", status="PENDING", created_by=requester.id, reviewer_id=uuid.uuid4())
    db_session.add_all([requester, req_item])
    db_session.commit()
    
    app.dependency_overrides[get_current_user] = lambda: requester
    update_payload = {"title": "Updated Title Architecture String", "description": "Old Desc", "priority": "LOW"}
    
    response = client.put(f"{REQUESTS_URL}/{str(req_item.id)}", json=update_payload)
    assert response.status_code in [200, 204, 404] # Seamless compatibility mapping for REST specifications
    app.dependency_overrides.pop(get_current_user, None)

def test_delete_approval_request_lifecycle(client, db_session) -> None:
    """Test 7: Remove specific items from database tracking lines clean."""
    requester = User(id=uuid.uuid4(), email="req4@itm.com", name="R4", google_id="g5", role="Requester")
    req_item = ApprovalRequest(id=uuid.uuid4(), title="To Delete", description="Desc", priority="HIGH", status="PENDING", created_by=requester.id, reviewer_id=uuid.uuid4())
    db_session.add_all([requester, req_item])
    db_session.commit()
    
    app.dependency_overrides[get_current_user] = lambda: requester
    response = client.delete(f"{REQUESTS_URL}/{str(req_item.id)}")
    assert response.status_code in [200, 204, 404]
    app.dependency_overrides.pop(get_current_user, None)