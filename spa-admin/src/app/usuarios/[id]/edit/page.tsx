"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { authService } from "../../../../lib/services/authService";
import { userService } from "../../../../lib/services/userService";
import { User } from "../../../../lib/models";

export default function EditUserPage() {
  const router = useRouter();
  const params = useParams();
  const userId = params.id ? parseInt(params.id as string, 10) : null; // Obter ID da URL

  const [user, setUser] = useState<User | null>(null);
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState(""); // Senha será opcional na edição
  const [admin, setAdmin] = useState(false);
  const [ativo, setAtivo] = useState(false); // Campo para soft delete
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    // Verificar se o usuário é admin e se o ID do usuário é válido
    if (!authService.isAdmin()) {
      router.push("/login");
      return;
    }
    if (userId === null || isNaN(userId)) {
      setErro("ID de usuário inválido.");
      setLoading(false);
      return;
    }

    // Buscar dados do usuário
    userService
      .getUserById(userId)
      .then((userData: User) => {
        setUser(userData);
        setNome(userData.nome);
        setAdmin(userData.admin);
        setAtivo(userData.ativo);
        setLoading(false);
      })
      .catch((err: unknown) => {
        console.error(`Erro ao carregar usuário ${userId}:`, err);
        setErro("Erro ao carregar dados do usuário. " + (err as Error).message);
        setLoading(false);
      });
  }, [userId, router]); // Dependências: userId e router

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro("");
    setMensagem("");

    if (userId === null || isNaN(userId)) {
      setErro("ID de usuário inválido para atualização.");
      return;
    }

    const updates: {
      nome?: string;
      senha?: string;
      admin?: boolean;
      ativo?: boolean;
    } = {};
    if (nome !== user?.nome) updates.nome = nome;
    if (senha) updates.senha = senha; // Atualiza senha apenas se campo preenchido
    if (admin !== user?.admin) updates.admin = admin;
    if (ativo !== user?.ativo) updates.ativo = ativo; // Atualiza status ativo

    // Não faz nada se não houver alterações e o campo senha estiver vazio
    if (Object.keys(updates).length === 0 && !senha) {
      setMensagem("Nenhuma alteração a ser salva.");
      return;
    }

    try {
      await userService.updateUser(userId, updates);
      setMensagem("Usuário atualizado com sucesso!");
      // Opcional: refetch dos dados para refletir quaisquer mudanças feitas pelo backend (ex: hash da senha)
      // userService.getUserById(userId).then(setUser).catch(console.error);
    } catch (err: unknown) {
      console.error(`Erro ao atualizar usuário ${userId}:`, err);
      if (err instanceof Error) {
        setErro("Erro ao atualizar usuário. " + err.message);
      } else {
        setErro("Ocorreu um erro desconhecido ao atualizar usuário.");
      }
    }
  };

  if (loading) {
    return <main className="p-6 max-w-md mx-auto">Carregando...</main>;
  }

  if (erro && !user) {
    // Mostrar erro apenas se não conseguiu carregar o usuário
    return <main className="p-6 max-w-md mx-auto text-red-600">{erro}</main>;
  }

  if (!user) {
    // Caso não encontre o usuário após carregar
    return (
      <main className="p-6 max-w-md mx-auto text-red-600">
        Usuário não encontrado.
      </main>
    );
  }

  return (
    <main className="max-w-md mx-auto mt-10 bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-2xl mb-6 font-semibold text-center text-gray-800">
        Editar Usuário: {user.nome} (ID: {user.id})
      </h1>
      {mensagem && (
        <p className="text-green-600 text-center mb-4">{mensagem}</p>
      )}
      {erro && <p className="text-red-600 text-center mb-4">{erro}</p>}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Nome:
          </label>
          <input
            type="text"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Senha (deixe em branco para manter a atual):
          </label>
          <input
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
          />
        </div>

        <div className="flex items-center">
          <input
            id="admin"
            name="admin"
            type="checkbox"
            checked={admin}
            onChange={(e) => setAdmin(e.target.checked)}
            className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="admin" className="ml-2 block text-sm text-gray-900">
            É Administrador
          </label>
        </div>

        <div className="flex items-center">
          <input
            id="ativo"
            name="ativo"
            type="checkbox"
            checked={ativo}
            onChange={(e) => setAtivo(e.target.checked)}
            className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="ativo" className="ml-2 block text-sm text-gray-900">
            Usuário Ativo
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Salvar Alterações
        </button>
      </form>

      <div className="mt-4">
        <button
          onClick={() => router.push("/dashboard")}
          className="w-full bg-gray-300 text-gray-800 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
        >
          Voltar para o Dashboard
        </button>
      </div>
    </main>
  );
}
