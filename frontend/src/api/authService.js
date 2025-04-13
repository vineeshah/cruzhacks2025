import apiClient from './client';

export const authService = {
    login: async (email, password) => {
        try {
            const response = await apiClient.post('/auth/login', { email, password });
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'An error occurred during login' };
        }
    },

    register: async (userData) => {
        try {
            const response = await apiClient.post('/auth/register', userData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'An error occurred during registration' };
        }
    },

    logout: () => {
        localStorage.removeItem('token');
    },

    getCurrentUser: async () => {
        try {
            const response = await apiClient.get('/auth/me');
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'An error occurred while fetching user data' };
        }
    }
}; 