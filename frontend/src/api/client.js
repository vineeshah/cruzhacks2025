import axios from 'axios';

// Create an axios instance with default config
const apiClient = axios.create({
    baseURL: 'http://localhost:5000/api',  // Your Flask backend URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to add the JWT token to requests
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Handle unauthorized access
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient; 