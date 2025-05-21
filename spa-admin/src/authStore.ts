import { create } from "zustand";
import { apiService } from "./lib/services/apiService"; // Importar apiService

interface AuthState {
  token: string | null;
  admin: boolean;
  isInitialized: boolean; // Adicionar um flag para indicar que o store foi inicializado
  setAuth: (token: string, admin: boolean) => void;
  logout: () => void;
  initializeAuth: () => Promise<void>; // Adicionar uma ação para inicializar/verificar
}

// Função auxiliar para ler o cookie
function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null; // Só funciona no navegador
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(";").shift() || null;
  return null;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: null,
  admin: false,
  isInitialized: false,

  setAuth: (token, admin) => set({ token, admin, isInitialized: true }), // Marca como inicializado ao definir auth

  logout: () => {
    // Chamar endpoint de logout no backend é feito no authService agora
    set({ token: null, admin: false, isInitialized: true }); // Marca como inicializado
    // Remover o cookie também é feito no authService/componente que chama logout
  },

  initializeAuth: async () => {
    const { isInitialized } = get();
    // Só inicializa se ainda não foi inicializado e não tem token na memória (evita loops)
    if (isInitialized) {
      return; // Já inicializado
    }

    const cookieToken = getCookie("token");

    if (cookieToken) {
      try {
        // Verificar o token com a API
        const data = await apiService.post<{
          valid: boolean;
          usuario_id: number;
          nome: string;
          admin: boolean;
        }>("/verify_token", { token: cookieToken });

        if (data.valid && data.admin) {
          // Se o token for válido e o usuário for admin, restaura o estado
          set({ token: cookieToken, admin: data.admin, isInitialized: true });
        } else {
          // Token inválido ou não admin, limpa qualquer token antigo e marca como inicializado
          set({ token: null, admin: false, isInitialized: true });
          // Opcional: remover o cookie inválido aqui também
          document.cookie = "token=; Max-Age=0; path=/";
        }
      } catch (error) {
        console.error("Erro ao verificar token na inicialização:", error);
        // Em caso de erro na verificação (ex: API offline), assume deslogado por segurança
        set({ token: null, admin: false, isInitialized: true });
        // Opcional: remover o cookie em caso de erro de verificação
        document.cookie = "token=; Max-Age=0; path=/";
      }
    } else {
      // Nenhum token no cookie, marca como inicializado (usuário deslogado)
      set({ token: null, admin: false, isInitialized: true });
    }
  },
}));
