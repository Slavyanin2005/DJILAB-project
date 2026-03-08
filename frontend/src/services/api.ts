import axios from 'axios';
import type { Service, Order, UserProfile } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // ← Отправлять куки сессии
});

// Перехватчик для добавления CSRF-токена
api.interceptors.request.use((config) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export const apiService = {
  // Услуги
  getServices: async (): Promise<Service[]> => {
    const response = await api.get('/services/');
    return response.data;
  },

  getService: async (id: number): Promise<Service> => {
    const response = await api.get(`/services/${id}/`);
    return response.data;
  },

  // Заказы
  getOrders: async (): Promise<Order[]> => {
    const response = await api.get('/orders/');
    return response.data;
  },

  getOrder: async (id: number): Promise<Order> => {
    const response = await api.get(`/orders/${id}/`);
    return response.data;
  },

  createOrder: async (): Promise<Order> => {
    // Отправляем пустой объект, т.к. бэкенд сам генерирует все поля
    const response = await api.post('/orders/', {});
    return response.data;
  },

  addToOrder: async (orderId: number, serviceId: number, quantity: number = 1): Promise<Order> => {
    const response = await api.post(`/orders/${orderId}/add_item/`, {
      service_id: serviceId,
      quantity,
    });
    return response.data;
  },

  updateQuantity: async (orderId: number, itemId: number, action: 'increase' | 'decrease'): Promise<Order> => {
    const response = await api.post(`/orders/${orderId}/update_item/`, {
      item_id: itemId,
      action,
    });
    return response.data;
  },

  removeItemFromOrder: async (orderId: number, itemId: number): Promise<Order> => {
    const response = await api.post(`/orders/${orderId}/remove_item/`, {
      item_id: itemId,
    });
    return response.data;
  },

  submitOrder: async (orderId: number): Promise<Order> => {
    const response = await api.post(`/orders/${orderId}/submit/`);
    return response.data;
  },

  deleteOrder: async (orderId: number): Promise<Order> => {
    const response = await api.post(`/orders/${orderId}/delete/`);
    return response.data;
  },

  // Профиль
  getProfile: async (): Promise<UserProfile | null> => {
    try {
      const response = await api.get('/profiles/');
      return response.data[0] || null;
    } catch {
      return null;
    }
  },
};
