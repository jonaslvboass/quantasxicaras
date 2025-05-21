"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "../../../authStore";
import { authService } from "../../lib/services/authService";

export default function LoginPage() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro("");
    try {
      const success = await authService.login(nome, senha);
      if (success) {
        document.cookie = `token=${useAuthStore.getState().token}; path=/`;
        router.push("/dashboard");
      } else {
        setErro("Nome ou senha inválidos, ou usuário não é administrador.");
      }
    } catch (err) {
      setErro("Erro no login: " + (err as Error).message);
    }
  }

  return (
    <main className="max-w-md mx-auto mt-20 bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-2xl mb-6 text-center font-semibold text-gray-800">
        Login Admin
      </h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome"
          className="border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
        />
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="Senha"
          className="border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
        />
        <button className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Entrar
        </button>
        {erro && <p className="text-red-500 text-center">{erro}</p>}
      </form>
    </main>
  );
}
