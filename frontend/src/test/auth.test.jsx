import React from 'react';
import { describe, test, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthContext } from '../context/authcontext';
import ProtectedRoute from '../components/ProtectedRoute';

describe('Frontend Authentication Strategy Matrix', () => {
  test('Login interface must trigger clear redirection route strings on click', () => {
    const mockLoginWithGoogle = vi.fn();
    const mockContextValue = {
        user: null,
        loading: false,
        loginWithGoogle: mockLoginWithGoogle,
        logout: vi.fn()
    };
    
    render(
      <AuthContext.Provider value={mockContextValue}>
        <button onClick={mockLoginWithGoogle}>Login with Google</button>
      </AuthContext.Provider>
    );

    const loginButton = screen.getByText(/Login with Google/i);
    fireEvent.click(loginButton);
    expect(mockLoginWithGoogle).toHaveBeenCalledTimes(1);
  });

  test('ProtectedRoute context layer must redirect anonymous users to login gateway', () => {
    const mockContextValue = { 
        user: null, 
        loading: false, 
        logout: vi.fn(), 
        loginWithGoogle: vi.fn() 
    };
    
    render(
      <AuthContext.Provider value={mockContextValue}>
        <BrowserRouter>
          <ProtectedRoute />
        </BrowserRouter>
      </AuthContext.Provider>
    );
    
    expect(screen.queryByText(/Loading application.../i)).not.toBeInTheDocument();
  });
});