import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { apiService } from '../services/api';
import type { Order } from '../types';

interface CartContextType {
  cartCount: number;
  draftOrder: Order | null;
  loading: boolean;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [cartCount, setCartCount] = useState(0);
  const [draftOrder, setDraftOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshCart = async () => {
    try {
      const orders = await apiService.getOrders();
      const draft = orders.find(o => o.status === 'draft');
      setDraftOrder(draft || null);
      setCartCount(draft?.items_count || 0);
    } catch (error) {
      console.error('Failed to refresh cart:', error);
      setCartCount(0);
      setDraftOrder(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshCart();
  }, []);

  return (
    <CartContext.Provider value={{ cartCount, draftOrder, loading, refreshCart }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = (): CartContextType => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
