"use client";
import { useEffect, useState } from "react";
import { useAuthStore } from "../../../authStore";
import { useRouter } from "next/navigation";
import { authService } from "../../lib/services/authService";
import { userService } from "../../lib/services/userService";
import { User } from "../../lib/models";

const USERS_PER_PAGE = 5;

export default function Dashboard() {
  const [usuarios, setUsuarios] = useState<User[]>([]);
  const [erro, setErro] = useState("");
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { token, logout } = useAuthStore();
  const router = useRouter();

  const [currentPage, setCurrentPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async (page: number) => {
    setLoading(true);
    setErro("");
    const offset = (page - 1) * USERS_PER_PAGE;
    try {
      const response = await userService.listUsers(USERS_PER_PAGE, offset);
      setUsuarios(response.usuarios);
      setTotalUsers(response.total);
      setLoading(false);
    } catch (err: unknown) {
      console.error("Erro ao buscar usuários paginados:", err);
      if (err instanceof Error) {
        setErro("Erro ao carregar usuários. " + err.message);
      } else {
        setErro("Ocorreu um erro desconhecido ao carregar usuários.");
      }
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authService.isAdmin()) {
      router.push("/login");
      return;
    }
    fetchUsers(currentPage);
  }, [currentPage, router]);

  const handleLogout = () => {
    logout();
    document.cookie = "token=; Max-Age=0; path=/";
    router.push("/login");
  };

  const handleBlockUser = async (userId: number) => {
    if (!confirm("Tem certeza que deseja bloquear este usuário?")) return;
    setErro("");
    try {
      await userService.blockUser(userId);
      fetchUsers(currentPage);
    } catch (err: unknown) {
      console.error(`Erro ao bloquear usuário ${userId}:`, err);
      if (err instanceof Error) {
        setErro("Erro ao bloquear usuário. " + err.message);
      } else {
        setErro("Ocorreu um erro desconhecido ao bloquear usuário.");
      }
    }
  };

  const handleUnblockUser = async (userId: number) => {
    if (!confirm("Tem certeza que deseja desbloquear este usuário?")) return;
    setErro("");
    try {
      await userService.unblockUser(userId);
      fetchUsers(currentPage);
    } catch (err: unknown) {
      console.error(`Erro ao desbloquear usuário ${userId}:`, err);
      if (err instanceof Error) {
        setErro("Erro ao desbloquear usuário. " + err.message);
      } else {
        setErro("Ocorreu um erro desconhecido ao desbloquear usuário.");
      }
    }
  };

  const totalPages = Math.ceil(totalUsers / USERS_PER_PAGE);

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <main className="p-6 max-w-4xl mx-auto bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6 border-b pb-4 border-gray-200">
        <h1 className="text-2xl font-semibold text-gray-800">Usuários</h1>
        <div className="flex gap-4">
          <button
            onClick={() => router.push("/cadastro")}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Novo Usuário
          </button>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Sair
          </button>
        </div>
      </div>
      {erro && <p className="text-red-500 mb-4">{erro}</p>}
      {loading ? (
        <p>Carregando usuários...</p>
      ) : (
        <table className="w-full table-auto border-collapse border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-3 border border-gray-300 text-left text-sm font-semibold text-gray-700">
                ID
              </th>
              <th className="p-3 border border-gray-300 text-left text-sm font-semibold text-gray-700">
                Nome
              </th>
              <th className="p-3 border border-gray-300 text-left text-sm font-semibold text-gray-700">
                Admin
              </th>
              <th className="p-3 border border-gray-300 text-left text-sm font-semibold text-gray-700">
                Ativo
              </th>
              <th className="p-3 border border-gray-300 text-left text-sm font-semibold text-gray-700">
                Ações
              </th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((u) => (
              <tr key={u.id} className="even:bg-gray-50 hover:bg-gray-100">
                <td className="p-3 border border-gray-300 text-sm text-gray-700">
                  {u.id}
                </td>
                <td className="p-3 border border-gray-300 text-sm text-gray-700">
                  {u.nome}
                </td>
                <td className="p-3 border border-gray-300 text-sm text-gray-700">
                  {u.admin ? "Sim" : "Não"}
                </td>
                <td className="p-3 border border-gray-300 text-sm text-gray-700">
                  {u.ativo ? "Sim" : "Não"}
                </td>
                <td className="p-3 border border-gray-300 flex gap-2 items-center">
                  <button
                    onClick={() => router.push(`/usuarios/${u.id}/edit`)}
                    className="bg-blue-500 text-white px-3 py-1 rounded-md text-sm hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    Editar
                  </button>
                  {u.ativo ? (
                    <button
                      onClick={() => handleBlockUser(u.id)}
                      className="bg-yellow-500 text-white px-3 py-1 rounded-md text-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500"
                    >
                      Bloquear
                    </button>
                  ) : (
                    <button
                      onClick={() => handleUnblockUser(u.id)}
                      className="bg-green-500 text-white px-3 py-1 rounded-md text-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
                    >
                      Desbloquear
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!loading && totalPages > 1 && (
        <div className="flex justify-center items-center mt-6 gap-4">
          <button
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>
          <span className="text-gray-700">
            Página {currentPage} de {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Próxima
          </button>
        </div>
      )}
    </main>
  );
}
