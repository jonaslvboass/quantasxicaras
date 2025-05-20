"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "../../../authStore";

export default function LoginPage() {
  const [nome, setNome] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:5001/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, senha }),
      });
      const data = await res.json();
      if (!res.ok || !data.admin) {
        setErro("Apenas administradores podem acessar.");
        return;
      }
      setAuth(data.token, data.admin);
      document.cookie = `token=${data.token}; path=/`;
      router.push("/dashboard");
    } catch (err) {
      setErro("Erro no login: " + err);
    }
  }

  return (
    <main className="max-w-md mx-auto mt-20">
      <h1 className="text-2xl mb-4">Login Admin</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome"
          className="border p-2"
        />
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          placeholder="Senha"
          className="border p-2"
        />
        <button className="bg-blue-600 text-white p-2 rounded">Entrar</button>
        {erro && <p className="text-red-500">{erro}</p>}
      </form>
    </main>
  );
}
