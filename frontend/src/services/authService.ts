import type { TokenResponse } from "../types/auth"

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error((err as { detail?: string }).detail ?? "Request failed")
  }
  return res.json() as Promise<T>
}

export const authService = {
  register: (email: string, password: string) =>
    post<TokenResponse>("/auth/register", { email, password }),
  login: (email: string, password: string) =>
    post<TokenResponse>("/auth/login", { email, password }),
}
