import { defineStore } from "pinia";
import axios from "axios";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    unreadCount: 0,
    pendingCount: 0,
  }),
  actions: {
    async fetchUnreadCount() {
      try {
        const response = await axios.get("/api/notifications/unread_count/");
        this.unreadCount = response.data.count;
        console.log("Количество непрочитанных уведомлений:", this.unreadCount);
      } catch (error) {
        console.error("Ошибка при загрузке количества уведомлений:", error);
      }
    },
    decrementUnreadCount() {
      if (this.unreadCount > 0) {
        this.unreadCount--;
      }
    },

    async fetchPendingCount() {
      try {
        const response = await axios.get(
          "/api/teacher-applications/pending_count/"
        );
        this.pendingCount = response.data.count;
        console.log("Количество непрочитанных заявок:", this.pendingCount);
      } catch (error) {
        console.error("Ошибка при загрузке количества заявок:", error);
      }
    },
    decrementPendingCount() {
      if (this.pendingCount > 0) {
        this.pendingCount--;
      }
    },
  },
});
