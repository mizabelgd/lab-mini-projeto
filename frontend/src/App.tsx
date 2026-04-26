import { useCallback, useEffect, useState } from "react"
import { TaskCard } from "./components/TaskCard"
import { TaskForm } from "./components/TaskForm"
import { taskService } from "./services/taskService"
import type { Task, TaskCreate, TaskStatus, TaskUpdate } from "./types/task"

type Filter = TaskStatus | "all"

const FILTERS: { label: string; value: Filter }[] = [
  { label: "Todas", value: "all" },
  { label: "Pendentes", value: "pending" },
  { label: "Concluídas", value: "completed" },
]

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [filter, setFilter] = useState<Filter>("all")
  const [loadError, setLoadError] = useState<string | null>(null)

  const loadTasks = useCallback(async () => {
    setLoadError(null)
    try {
      const data = await taskService.list(filter === "all" ? null : filter)
      setTasks(data)
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : "Erro ao carregar tarefas")
    }
  }, [filter])

  useEffect(() => {
    void loadTasks()
  }, [loadTasks])

  async function handleCreate(data: TaskCreate) {
    const task = await taskService.create(data)
    setTasks((prev) => [task, ...prev])
  }

  async function handleComplete(id: number) {
    const task = await taskService.complete(id)
    setTasks((prev) => prev.map((t) => (t.id === id ? task : t)))
  }

  async function handleUpdate(id: number, data: TaskUpdate) {
    const task = await taskService.update(id, data)
    setTasks((prev) => prev.map((t) => (t.id === id ? task : t)))
  }

  async function handleDelete(id: number) {
    await taskService.remove(id)
    setTasks((prev) => prev.filter((t) => t.id !== id))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-900">task-api</h1>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8 flex flex-col gap-6">
        <TaskForm onSubmit={handleCreate} />

        <div className="flex gap-2">
          {FILTERS.map(({ label, value }) => (
            <button
              key={value}
              onClick={() => setFilter(value)}
              className={`text-sm px-4 py-1.5 rounded-full font-medium transition-colors ${
                filter === value
                  ? "bg-indigo-600 text-white"
                  : "bg-white text-gray-600 border border-gray-200 hover:border-gray-400"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {loadError && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
            {loadError}
          </div>
        )}

        {tasks.length === 0 && !loadError ? (
          <p className="text-sm text-gray-400 text-center py-12">Nenhuma tarefa encontrada.</p>
        ) : (
          <div className="flex flex-col gap-3">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onComplete={handleComplete}
                onUpdate={handleUpdate}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
