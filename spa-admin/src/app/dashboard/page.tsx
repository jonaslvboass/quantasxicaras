"use client";
import { useEffect, useState } from "react";
import { useAuthStore } from "../../../authStore";
import { apiFetch } from "../../lib/api";
import { useRouter } from "next/navigation";

interface Usuario {
  id: number;
  nome: string;
  admin: boolean;
  ativo: boolean;
}

export default function Dashboard() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [erro, setErro] = useState("");
  const { token, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!token) return;
    apiFetch("/usuarios", token)
      .then(setUsuarios)
      .catch((err) => setErro(err.message));
  }, [token]);

  const handleLogout = () => {
    logout();
    document.cookie = "token=; Max-Age=0; path=/";
    router.push("/login");
  };

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Usuários</h1>
        <button
          onClick={handleLogout}
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Sair
        </button>
      </div>
      {erro && <p className="text-red-500">{erro}</p>}
      <table className="w-full table-auto border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Nome</th>
            <th className="p-2 border">Admin</th>
            <th className="p-2 border">Ativo</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((u) => (
            <tr key={u.id}>
              <td className="p-2 border">{u.id}</td>
              <td className="p-2 border">{u.nome}</td>
              <td className="p-2 border">{u.admin ? "Sim" : "Não"}</td>
              <td className="p-2 border">{u.ativo ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
