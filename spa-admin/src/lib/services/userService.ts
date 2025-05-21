import { apiService } from "./apiService";
import { User } from "../models";

interface CreateUserResponse {
  message: string;
  usuario_id: number; // Assumindo que o ID retornado é numérico
  admin: boolean;
}

interface PaginatedUsersResponse {
  usuarios: User[];
  total: number;
  limit: number;
  offset: number;
}

export const userService = {
  async createUser(
    nome: string,
    senha: string,
    admin: boolean
  ): Promise<CreateUserResponse> {
    try {
      // A lógica de verificação se o usuário logado é admin ficará no componente
      // ou em um hook, usando authService.isAdmin()
      const response = await apiService.post<CreateUserResponse>("/register", {
        nome,
        senha,
        admin,
      });
      return response;
    } catch (error) {
      console.error("Erro ao criar usuário:", error);
      throw error; // Repropaga o erro para o componente lidar
    }
  },

  async listUsers(
    limit: number,
    offset: number
  ): Promise<PaginatedUsersResponse> {
    try {
      // Passar limit e offset como query parameters
      const response = await apiService.get<PaginatedUsersResponse>(
        `/usuarios?limit=${limit}&offset=${offset}`
      );
      return response;
    } catch (error) {
      console.error("Erro ao listar usuários paginados:", error);
      throw error; // Repropaga o erro
    }
  },

  async getUserById(id: number): Promise<User> {
    try {
      const user = await apiService.get<User>(`/usuarios/${id}`);
      return user;
    } catch (error) {
      console.error(`Erro ao buscar usuário ${id}:`, error);
      throw error;
    }
  },

  async updateUser(
    id: number,
    updates: { nome?: string; senha?: string; admin?: boolean; ativo?: boolean }
  ): Promise<void> {
    try {
      await apiService.put<void>(`/usuarios/${id}`, updates);
    } catch (error) {
      console.error(`Erro ao atualizar usuário ${id}:`, error);
      throw error;
    }
  },

  async blockUser(id: number): Promise<void> {
    try {
      await apiService.post<void>(`/usuarios/${id}/bloquear`);
    } catch (error) {
      console.error(`Erro ao bloquear usuário ${id}:`, error);
      throw error;
    }
  },

  async unblockUser(id: number): Promise<void> {
    try {
      await apiService.post<void>(`/usuarios/${id}/desbloquear`);
    } catch (error) {
      console.error(`Erro ao desbloquear usuário ${id}:`, error);
      throw error;
    }
  },

  // TODO: Adicionar métodos para listar, editar e soft delete usuários
};
