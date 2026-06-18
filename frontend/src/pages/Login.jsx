import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const { user, loading, loginWithGoogle } = useAuth();

  // If user is already logged in, redirect them to dashboard
  if (!loading && user) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '100px' }}>
      <h1>Csyrus Workflow Approval</h1>
      <p>Please sign in to continue</p>
      <button 
        onClick={loginWithGoogle} 
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#4285F4',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px'
        }}
      >
        Sign in with Google
      </button>
    </div>
  );
};

export default Login;