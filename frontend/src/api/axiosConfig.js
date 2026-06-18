import axios from 'axios';

// Create a central axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', //  FastAPI backend address
  withCredentials: true,  // Include cookies for authentication
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor: 401 (Unauthorized) responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token/state handling will be done in AuthContext
      console.warn("Unauthorized access. Redirecting to login...");
    }
    return Promise.reject(error);
  }
);

export default apiClient;