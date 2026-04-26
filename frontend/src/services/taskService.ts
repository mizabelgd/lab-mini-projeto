import type { Task, TaskCreate, TaskStatus, TaskUpdate } from "../types/task"

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error((body as { detail?: string }).detail ?? "Request failed")
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export const taskService = {
  list: (status?: TaskStatus | null) => {
    const qs = status ? `?status=${status}` : ""
    return request<Task[]>(`/tasks${qs}`)
  },
  create: (data: TaskCreate) =>
    request<Task>("/tasks", { method: "POST", body: JSON.stringify(data) }),
  update: (id: number, data: TaskUpdate) =>
    request<Task>(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  complete: (id: number) =>
    request<Task>(`/tasks/${id}/complete`, { method: "PATCH" }),
  remove: (id: number) =>
    request<void>(`/tasks/${id}`, { method: "DELETE" }),
}
