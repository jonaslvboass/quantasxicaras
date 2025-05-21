import { useAuthStore } from "../../../authStore";

const API_BASE_URL = "http://localhost:5001"; // TODO: Mover para variável de ambiente

export const apiService = {
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>("GET", endpoint);
  },

  async post<T>(endpoint: string, data?: object): Promise<T> {
    return this.request<T>("POST", endpoint, data);
  },

  async put<T>(endpoint: string, data?: object): Promise<T> {
    return this.request<T>("PUT", endpoint, data);
  },

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>("DELETE", endpoint);
  },

  async request<T>(
    method: string,
    endpoint: string,
    data?: object
  ): Promise<T> {
    const { token } = useAuthStore.getState(); // Acessa o estado do store

    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config: RequestInit = {
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }

    // Tenta retornar JSON, mas lida com respostas vazias
    const text = await response.text();
    try {
      return text ? (JSON.parse(text) as T) : ({} as T); // Cast para tipo T
    } catch {
      // Se a resposta não for JSON, mas a requisição foi bem sucedida (ex: 204 No Content)
      // Retornamos um objeto vazio ou null, dependendo do esperado. Aqui, retornamos objeto vazio.
      return {} as T; // Retorna um objeto vazio tipado como T
    }
  },
};
