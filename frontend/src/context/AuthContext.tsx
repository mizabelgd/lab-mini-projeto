import { createContext, useContext, useState, type ReactNode } from "react"

interface AuthContextValue {
  token: string | null
  login: (token: string) => void
  logout: () => void
}

const TOKEN_KEY = "task_api_token"

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY))

  function login(t: string) {
    localStorage.setItem(TOKEN_KEY, t)
    setToken(t)
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
  }

  return <AuthContext.Provider value={{ token, login, logout }}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
