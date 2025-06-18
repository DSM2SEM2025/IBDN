import { create } from 'zustand';
import * as notificacaoService from '../services/notificacaoService';

const useNotificationStore = create((set, get) => ({
    notifications: [],
    unreadCount: 0,
    isPanelOpen: false,

    // Ação para buscar as notificações
    fetchNotifications: async (empresaId) => {
        if (!empresaId) {
            set({ notifications: [], unreadCount: 0 });
            return;
        }
        try {
            const data = await notificacaoService.listarNotificacoesEmpresa(empresaId);
            const unread = data.filter(n => !n.lida).length;
            set({ notifications: data, unreadCount: unread });
        } catch (error) {
            console.error("Falha ao buscar notificações:", error);
            set({ notifications: [], unreadCount: 0 });
        }
    },

    // Ação para marcar como lida
    markAsRead: async (notificationId) => {
        try {
            await notificacaoService.atualizarNotificacao(notificationId, { lida: true });
            // Atualiza o estado localmente para uma resposta visual instantânea
            set(state => {
                const updatedNotifications = state.notifications.map(n =>
                    n.id === notificationId ? { ...n, lida: true } : n
                );
                const unread = updatedNotifications.filter(n => !n.lida).length;
                return { notifications: updatedNotifications, unreadCount: unread };
            });
        } catch (error) {
            console.error("Erro ao marcar notificação como lida:", error);
        }
    },

    togglePanel: () => set(state => ({ isPanelOpen: !state.isPanelOpen })),
    closePanel: () => set({ isPanelOpen: false }),
}));

export default useNotificationStore;