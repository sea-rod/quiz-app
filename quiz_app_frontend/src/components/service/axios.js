// lib/api.js
import axios from 'axios';
import { auth } from './firebase.js'; // Your Firebase config file
import Cookies from 'js-cookie';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_FASTAPI_URL || 'http://localhost:8000', // Update this later
  timeout: 100000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach the token
apiClient.interceptors.request.use(
  async (config) => {
    let token = Cookies.get('access_token'); // Get token from cookie
    if (!token && auth.currentUser) {
      token = await auth.currentUser.getIdToken(); // Fallback to Firebase
      Cookies.set('access_token', token, {
        secure: true,
        sameSite: 'Strict',
        path: '/',
      });
    }
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else if (!config.skipAuth) {
      throw new Error('No token available');
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Prevent infinite loop

      try {
        const user = firebase.auth().currentUser;
        if (user) {
          // Force refresh the ID token using Firebase
          const newToken = await user.getIdToken(true);
          Cookies.set('access_token', newToken, {
            secure: true,
            sameSite: 'Strict',
            path: '/',
          });
          // Update the Authorization header and retry the request
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return apiClient(originalRequest);
        } else {
          // No user, redirect to login
          window.location.href = '/login';
          return Promise.reject(error);
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        firebase.auth().signOut();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;