"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "../../../authStore";
import { apiFetch } from "../../lib/api";

export default function CadastroPage() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [admin, setAdmin] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const router = useRouter();
  const { token } = useAuthStore();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro("");
    setMensagem("");
    try {
      await apiFetch("/register", token || "", {
        method: "POST",
        body: JSON.stringify({ nome, senha, admin }),
      });
      setMensagem("Usuário cadastrado com sucesso!");
      setNome("");
      setSenha("");
      setAdmin(false);
      setTimeout(() => router.push("/dashboard"), 1000);
    } catch (err: any) {
      setErro(err.message);
    }
  }

  return (
    <main className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl mb-4 font-semibold">Cadastrar novo usuário</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome"
          className="border p-2"
          required
        />
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="Senha"
          className="border p-2"
          required
        />
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={admin}
            onChange={(e) => setAdmin(e.target.checked)}
          />
          Administrador
        </label>
        <button type="submit" className="bg-green-600 text-white p-2 rounded">
          Cadastrar
        </button>
        {mensagem && <p className="text-green-600">{mensagem}</p>}
        {erro && <p className="text-red-600">{erro}</p>}
      </form>
    </main>
  );
}
