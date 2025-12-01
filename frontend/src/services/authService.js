import api from './api';

export const authService = {
    login: async (cedula, password) => {
        const response = await api.post('/auth/login/', { cedula, password });
        const { access, refresh, user } = response.data;

        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        localStorage.setItem('user', JSON.stringify(user));

        return user;
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    },

    getCurrentUser: async () => {
        const response = await api.get('/usuarios/me/');
        return response.data;
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('access_token');
    },

    getStoredUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    register: async (userData) => {
        const response = await api.post('/usuarios/register/', userData);
        return response.data;
    },
};
