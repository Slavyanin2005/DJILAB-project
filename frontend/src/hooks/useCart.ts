import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useCart = () => {
  const [cartCount, setCartCount] = useState(0);

  const loadCartCount = async () => {
    try {
      const orders = await apiService.getOrders();
      const draftOrder = orders.find(o => o.status === 'draft');
      setCartCount(draftOrder?.items_count || 0);
    } catch (error) {
      console.error('Failed to load cart count:', error);
      setCartCount(0);
    }
  };

  useEffect(() => {
    loadCartCount();
  }, []);

  return { cartCount, loadCartCount, setCartCount };
};
