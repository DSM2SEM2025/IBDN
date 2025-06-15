import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode'; // Precisaremos de uma biblioteca para decodificar o token

const useAuthStore = create((set) => ({
    token: null,
    isAuthenticated: false,
    permissions: [], // NOVO: Estado para armazenar as permissões
    // Ação para fazer login: salva o token e extrai as permissões
    login: (token) => {
        try {
            const decodedToken = jwtDecode(token);
            const permissions = decodedToken.permissoes || [];
            console.log("Salvando token e permissões:", permissions);
            set({ token, isAuthenticated: true, permissions });
        } catch (error) {
            console.error("Token inválido:", error);
            set({ token: null, isAuthenticated: false, permissions: [] });
        }
    },
    // Ação para fazer logout: limpa tudo
    logout: () => set({ token: null, isAuthenticated: false, permissions: [] }),
}));

export default useAuthStore;