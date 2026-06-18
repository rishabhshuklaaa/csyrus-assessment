import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
// INTEGRATION: Consuming centralized api routing networks safely
import apiClient from '../services/api';
import RequestList from '../components/RequestList';
import RequestForm from '../components/RequestForm';

const RequesterDashboard = () => {
  const { user, logout } = useAuth();
  const [requests, setRequests] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingRequest, setEditingRequest] = useState(null);

  const fetchRequests = async () => {
    try {
      const response = await apiClient.get('/requests');
      setRequests(response.data);
    } catch (error) {
      console.error("Failed to fetch requests", error);
    }
  };

  useEffect(() => {
    fetchRequests();
    
    // Polling auto-sync routine
    const interval = setInterval(() => {
      fetchRequests();
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const handleCreate = async (formData) => {
    try {
      await apiClient.post('/requests', formData);
      setIsFormOpen(false);
      fetchRequests();
    } catch (error) {
      alert("Failed to create request: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const handleUpdate = async (formData) => {
    try {
      await apiClient.put(`/requests/${formData.id}`, formData);
      setEditingRequest(null);
      setIsFormOpen(false);
      fetchRequests();
    } catch (error) {
      alert("Failed to update: " + (error.response?.data?.detail || "Unknown error"));
    }
  };

  const handleDelete = async (id) => {
    if(window.confirm("Are you sure you want to delete this request?")) {
      try {
        await apiClient.delete(`/requests/${id}`);
        fetchRequests();
      } catch (error) {
        alert("Failed to delete");
      }
    }
  };

  const openEditModal = (request) => {
    setEditingRequest(request);
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
    setEditingRequest(null);
  };

  return (
    <div className="container">
      <div className="header">
        <div className="header-info">
          <h1>Requester Dashboard</h1>
          <p>Welcome back, {user?.name} ({user?.role})</p>
        </div>
        <div style={{ display: 'flex', gap: '15px' }}>
          <button className="btn btn-primary" onClick={() => setIsFormOpen(true)}>+ New Request</button>
          <button className="btn btn-danger" onClick={logout}>Logout</button>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ background: 'white', padding: '15px 25px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
          <h3 style={{ color: '#7f8c8d', fontSize: '14px' }}>Total Requests</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#2c3e50' }}>{requests.length}</p>
        </div>
      </div>

      <RequestList 
        requests={requests} 
        onEdit={openEditModal} 
        onDelete={handleDelete} 
      />

      {isFormOpen && (
        <RequestForm 
          user={user}
          initialData={editingRequest} 
          onSubmit={editingRequest ? handleUpdate : handleCreate} 
          onCancel={closeForm} 
        />
      )}
    </div>
  );
};

export default RequesterDashboard;