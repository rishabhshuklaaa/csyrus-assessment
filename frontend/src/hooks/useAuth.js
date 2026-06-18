import { useContext } from 'react';
import { AuthContext } from '../context/authcontext';

/**
 * Custom hook to consume the global Auth Context state values safely.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be executed within an explicit AuthProvider wrapper constraint.');
  }
  
  // Destructuring common properties from your existing auth context state layout
  const { user, loading, logout } = context;
  
  return {
    user,
    loading,
    logout,
    isReviewer: user?.role === 'Reviewer' || user?.email?.endsWith('@samayak.com'),
    isRequester: user?.role === 'Requester',
  };
}