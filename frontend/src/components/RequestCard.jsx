import React from 'react';
import { getPriorityStyles } from "../utils/formatters.js";

const RequestCard = ({ request, onEdit, onDelete }) => {
  const getStatusBadge = (status) => {
    switch (status) {
      case 'APPROVED': return 'badge badge-approved';
      case 'REJECTED': return 'badge badge-rejected';
      default: return 'badge badge-pending';
    }
  };

  return (
    <div className="request-card">
      <div className="card-header">
        <div>
          <h3 className="card-title">{request.title}</h3>
          <span className={getStatusBadge(request.status)}>{request.status}</span>
          {/* UTILIS CONTEXT LINK: Dynamically parsing priority tags cleanly */}
          <span className={getPriorityStyles(request.priority)}>{request.priority}</span>
        </div>
      </div>
      <p className="card-desc">{request.description}</p>
      
      <div className="card-footer">
        <small style={{ color: '#7f8c8d' }}>Reviewer: {request.reviewer_id.substring(0,8)}...</small>
        
        {/* Only show actions if status is PENDING */}
        {request.status === 'PENDING' && (
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="btn btn-secondary" onClick={() => onEdit(request)}>Edit</button>
            <button className="btn btn-danger" onClick={() => onDelete(request.id)}>Delete</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RequestCard;