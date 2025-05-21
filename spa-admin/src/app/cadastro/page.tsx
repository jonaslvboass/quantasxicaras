"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { userService } from "../../lib/services/userService";
import { authService } from "../../lib/services/authService";

export default function CadastroPage() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [admin, setAdmin] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const router = useRouter();

  useState(() => {
    if (!authService.isAdmin()) {
      router.push("/login");
    }
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro("");
    setMensagem("");

    if (!authService.isAdmin()) {
      setErro("Você não tem permissão para cadastrar usuários.");
      return;
    }

    try {
      const response = await userService.createUser(nome, senha, admin);
      setMensagem(response.message);
      setNome("");
      setSenha("");
      setAdmin(false);
      if (authService.isAdmin()) {
        setTimeout(() => router.push("/dashboard"), 1000);
      } else {
        router.push("/login");
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErro(err.message);
      } else {
        setErro("Ocorreu um erro desconhecido ao cadastrar usuário.");
      }
    }
  }

  return (
    <main className="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-2xl mb-6 font-semibold text-center text-gray-800">
        Cadastrar novo usuário
      </h1>
      {mensagem && (
        <p className="text-green-600 text-center mb-4">{mensagem}</p>
      )}
      {erro && <p className="text-red-600 text-center mb-4">{erro}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome"
          className="border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
          required
        />
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="Senha"
          className="border border-gray-300 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
          required
        />
        <label className="flex items-center gap-2 text-gray-700">
          <input
            type="checkbox"
            checked={admin}
            onChange={(e) => setAdmin(e.target.checked)}
            className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          Administrador
        </label>
        <button
          type="submit"
          className="bg-green-600 text-white p-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          Cadastrar
        </button>
        <button
          type="button"
          onClick={() => router.push("/dashboard")}
          className="w-full bg-gray-300 text-gray-800 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
        >
          Cancelar
        </button>
      </form>
    </main>
  );
}
