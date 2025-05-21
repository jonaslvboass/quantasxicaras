import { apiService } from "./apiService";
import { useAuthStore } from "../../../authStore";

interface LoginResponse {
  token: string;
  admin: boolean;
}

export const authService = {
  async login(nome: string, senha: string): Promise<boolean> {
    try {
      const data = await apiService.post<LoginResponse>("/login", {
        nome,
        senha,
      });
      if (data.token && data.admin) {
        useAuthStore.getState().setAuth(data.token, data.admin);
        return true; // Login de admin bem-sucedido
      }
      // Se não for admin, ou não retornou token/admin
      return false;
    } catch (error) {
      console.error("Erro no login:", error);
      // Podemos adicionar um tratamento de erro mais sofisticado aqui
      throw error; // Repropaga o erro para o componente lidar
    }
  },

  logout() {
    // Chamar endpoint de logout na API
    apiService.post<void>("/logout").catch((error) => {
      // Logar erro, mas continuar com o logout local mesmo se a chamada falhar
      console.error("Erro ao chamar endpoint de logout:", error);
    });

    // Limpar estado local e cookie
    useAuthStore.getState().logout();
    document.cookie = "token=; Max-Age=0; path=/";
    // A navegação para a página de login será feita no componente que chama logout
  },

  isAdmin(): boolean {
    const { admin } = useAuthStore.getState();
    return admin;
  },
};
