import React, { useState, useEffect } from 'react';
import apiClient from '../api/axiosConfig';

const RequestForm = ({ onSubmit, onCancel, initialData, user }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'MEDIUM',
    reviewer_id: '' 
  });
  

  const [reviewers, setReviewers] = useState([]);

  useEffect(() => {
    
    const fetchReviewers = async () => {
      try {
        const response = await apiClient.get('/auth/reviewers');
        setReviewers(response.data);
        
        
        if (!initialData && response.data.length > 0) {
          setFormData(prev => ({ ...prev, reviewer_id: response.data[0].id }));
        }
      } catch (error) {
        console.error("Failed to fetch reviewers", error);
      }
    };
    fetchReviewers();

    
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2 style={{ marginBottom: '20px' }}>
          {initialData ? 'Edit Request' : 'Create New Request'}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Title</label>
            <input type="text" name="title" className="form-control" value={formData.title} onChange={handleChange} required />
          </div>
          
          <div className="form-group">
            <label>Description</label>
            <textarea name="description" className="form-control" rows="4" value={formData.description} onChange={handleChange} required />
          </div>
          
          <div className="form-group">
            <label>Priority</label>
            <select name="priority" className="form-control" value={formData.priority} onChange={handleChange}>
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
            </select>
          </div>
          
         
          <div className="form-group">
            <label>Assign to Reviewer</label>
            <select name="reviewer_id" className="form-control" value={formData.reviewer_id} onChange={handleChange} required>
              <option value="" disabled>Select a person</option>
              {reviewers.map(r => (
                <option key={r.id} value={r.id}>
                  {r.name} {r.id === user?.id ? '(You)' : ''}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
            <button type="submit" className="btn btn-primary">{initialData ? 'Update' : 'Submit'}</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RequestForm;
