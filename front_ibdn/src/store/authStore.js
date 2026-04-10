import { create } from 'zustand';

const useAuthStore = create((set) => ({
    token: null,
    isAuthenticated: false,
    user: null,

    // Login recebe o objeto de usuário diretamente (sem JWT)
    login: (userData) => {
        set({
            token: 'demo-token-ibdn',
            isAuthenticated: true,
            user: userData,
        });
    },

    // Logout limpa tudo
    logout: () => set({ token: null, isAuthenticated: false, user: null }),
}));

export default useAuthStore;