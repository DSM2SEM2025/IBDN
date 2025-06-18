import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

const useAuthStore = create((set) => ({
    token: null,
    isAuthenticated: false,
    user: null, // Alterado de 'permissions' para 'user' para guardar todo o payload

    // Ação de login atualizada
    login: (token) => {
        try {
            const decodedToken = jwtDecode(token);
            // Guarda o payload completo do utilizador, que inclui email, usuario_id, empresa_id e permissoes
            const user = {
                id: decodedToken.usuario_id,
                email: decodedToken.email,
                empresa_id: decodedToken.empresa_id,
                permissoes: decodedToken.permissoes || [],
            };
            console.log("Utilizador autenticado:", user);
            set({ token, isAuthenticated: true, user });
        } catch (error) {
            console.error("Token inválido:", error);
            set({ token: null, isAuthenticated: false, user: null });
        }
    },

    // Ação de logout limpa tudo
    logout: () => set({ token: null, isAuthenticated: false, user: null }),
}));

export default useAuthStore;