// authStore.ts
import { create } from "zustand";

interface AuthState {
  token: string | null;
  admin: boolean;
  setAuth: (token: string, admin: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  admin: false,
  setAuth: (token, admin) => set({ token, admin }),
  logout: () => set({ token: null, admin: false }),
}));
