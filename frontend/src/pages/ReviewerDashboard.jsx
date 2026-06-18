import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import apiClient from '../api/axiosConfig';

const ReviewerDashboard = () => {
  const { user, logout } = useAuth();
  const [requests, setRequests] = useState([]);
  const [actionModal, setActionModal] = useState({ isOpen: false, request: null, type: '' });
  const [comment, setComment] = useState('');

  const fetchAssignedRequests = async () => {
    try {
      const response = await apiClient.get('/reviewer/requests');
      setRequests(response.data);
    } catch (error) {
      console.error("Failed to fetch assigned requests", error);
    }
  };

  useEffect(() => {
    // 1. Initial fetch on page load
    fetchAssignedRequests();

    // 2. Auto-refresh every 5 seconds (Polling)
    const interval = setInterval(() => {
      fetchAssignedRequests();
    }, 5000);

    // 3. Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []); // Empty dependency array means this runs once on mount

  const handleAction = async (e) => {
    e.preventDefault();
    try {
      const endpoint = `/reviewer/requests/${actionModal.request.id}/${actionModal.type.toLowerCase()}`;
      await apiClient.post(endpoint, { comments: comment });
      
      // Reset and refresh immediately after action
      setActionModal({ isOpen: false, request: null, type: '' });
      setComment('');
      fetchAssignedRequests();
    } catch (error) {
      alert("Action failed: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'APPROVED': return 'badge badge-approved';
      case 'REJECTED': return 'badge badge-rejected';
      default: return 'badge badge-pending';
    }
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <div className="header-info">
          <h1>Admin / Reviewer Dashboard</h1>
          <p>Welcome, {user?.name} ({user?.role})</p>
        </div>
        <button className="btn btn-danger" onClick={logout}>Logout</button>
      </div>

      {/* Requests List */}
      <div className="requests-grid">
        {requests.length === 0 ? (
          <p style={{ color: '#7f8c8d' }}>No requests assigned to you yet.</p>
        ) : (
          requests.map((req) => (
            <div key={req.id} className="request-card">
              <div className="card-header">
                <div>
                  <h3 className="card-title">{req.title}</h3>
                  <span className={getStatusBadge(req.status)}>{req.status}</span>
                  <span className="badge badge-priority">{req.priority}</span>
                </div>
              </div>
              <p className="card-desc">{req.description}</p>
              
              <div className="card-footer">
                <small style={{ color: '#7f8c8d' }}>From: {req.created_by.substring(0,8)}...</small>
                
                {/* Show Approve/Reject buttons only if status is PENDING */}
                {req.status === 'PENDING' && (
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button 
                      className="btn btn-primary" 
                      style={{ backgroundColor: '#2ecc71' }} 
                      onClick={() => setActionModal({ isOpen: true, request: req, type: 'APPROVE' })}
                    >
                      Approve
                    </button>
                    <button 
                      className="btn btn-danger" 
                      onClick={() => setActionModal({ isOpen: true, request: req, type: 'REJECT' })}
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Approve/Reject Action Modal */}
      {actionModal.isOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2 style={{ marginBottom: '15px' }}>
              {actionModal.type === 'APPROVE' ? 'Approve Request' : 'Reject Request'}
            </h2>
            <form onSubmit={handleAction}>
              <div className="form-group">
                <label>Add a Comment (Optional for Approve, recommended for Reject)</label>
                <textarea 
                  className="form-control" 
                  rows="3" 
                  value={comment} 
                  onChange={(e) => setComment(e.target.value)} 
                  placeholder="e.g., Looks good to me!" 
                  required={actionModal.type === 'REJECT'} 
                />
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setActionModal({ isOpen: false, request: null, type: '' })}>Cancel</button>
                <button type="submit" className={`btn ${actionModal.type === 'APPROVE' ? 'btn-primary' : 'btn-danger'}`}>
                  Confirm {actionModal.type}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReviewerDashboard;