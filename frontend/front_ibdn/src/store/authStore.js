import { create } from 'zustand'; // Correção: Importando como um módulo nomeado

const useAuthStore = create((set) => ({
    token: null,
    isAuthenticated: false,
    // Ação para fazer login: salva o token e atualiza o estado de autenticação
    login: (token) => {
        console.log("Salvando token na store:", token);
        set({ token, isAuthenticated: true });
    },
    // Ação para fazer logout: limpa o token e o estado de autenticação
    logout: () => set({ token: null, isAuthenticated: false }),
}));

export default useAuthStore;
