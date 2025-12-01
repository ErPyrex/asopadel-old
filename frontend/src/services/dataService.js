import api from './api';

export const torneoService = {
    getAll: async (params = {}) => {
        const response = await api.get('/torneos/', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/torneos/${id}/`);
        return response.data;
    },

    create: async (data) => {
        const response = await api.post('/torneos/', data);
        return response.data;
    },

    update: async (id, data) => {
        const response = await api.put(`/torneos/${id}/`, data);
        return response.data;
    },

    delete: async (id) => {
        await api.delete(`/torneos/${id}/`);
    },
};

export const canchaService = {
    getAll: async () => {
        const response = await api.get('/canchas/');
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/canchas/${id}/`);
        return response.data;
    },

    create: async (data) => {
        const response = await api.post('/canchas/', data);
        return response.data;
    },
};

export const partidoService = {
    getAll: async (params = {}) => {
        const response = await api.get('/partidos/', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/partidos/${id}/`);
        return response.data;
    },
};

export const usuarioService = {
    getAll: async () => {
        const response = await api.get('/usuarios/');
        return response.data;
    },

    getById: async (id) => {
        const response = await api.get(`/usuarios/${id}/`);
        return response.data;
    },
};
