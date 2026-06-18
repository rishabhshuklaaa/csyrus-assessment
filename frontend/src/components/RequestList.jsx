import React from 'react';
import RequestCard from './RequestCard';

const RequestList = ({ requests, onEdit, onDelete }) => {
  if (!requests || requests.length === 0) {
    return <div style={{ textAlign: 'center', padding: '40px', color: '#7f8c8d' }}>No requests found. Create one to get started!</div>;
  }

  return (
    <div className="requests-grid">
      {requests.map((req) => (
        <RequestCard key={req.id} request={req} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </div>
  );
};

export default RequestList;