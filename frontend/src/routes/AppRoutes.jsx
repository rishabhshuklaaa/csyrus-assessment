import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from '../pages/Login';
import RequesterDashboard from '../pages/RequesterDashboard';
import ReviewerDashboard from '../pages/ReviewerDashboard';
import ProtectedRoute from '../components/ProtectedRoute';
import { useAuth } from '../context/AuthContext';

// Dashboard decider 
const DashboardRouter = () => {
  const { user } = useAuth();
  
  if (user?.role === 'Reviewer') {
    return <ReviewerDashboard />;
  }
  return <RequesterDashboard />;
};

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route element={<ProtectedRoute />}>
          {/* Dashboard route hit hote hi DashboardRouter decision lega */}
          <Route path="/dashboard" element={<DashboardRouter />} /> 
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Route>

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;