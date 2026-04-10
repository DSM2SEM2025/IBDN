import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      isAuthenticated: false,
      user: null,

      login: (userData, token) => {
        set({ token, isAuthenticated: true, user: userData });
      },

      logout: () => set({ token: null, isAuthenticated: false, user: null }),
    }),
    { name: 'auth-storage' }
  )
);

export default useAuthStore;