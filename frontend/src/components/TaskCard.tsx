import { useState } from "react"
import type { Task, TaskUpdate } from "../types/task"

interface Props {
  task: Task
  onComplete: (id: number) => Promise<void>
  onUpdate: (id: number, data: TaskUpdate) => Promise<void>
  onDelete: (id: number) => Promise<void>
}

export function TaskCard({ task, onComplete, onUpdate, onDelete }: Props) {
  const [editing, setEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description ?? "")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const isCompleted = task.status === "completed"

  async function handleSave() {
    if (!title.trim()) return
    setLoading(true)
    setError(null)
    try {
      await onUpdate(task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      })
      setEditing(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao salvar")
    } finally {
      setLoading(false)
    }
  }

  function handleCancel() {
    setTitle(task.title)
    setDescription(task.description ?? "")
    setError(null)
    setEditing(false)
  }

  async function handle(action: () => Promise<void>) {
    setLoading(true)
    setError(null)
    try {
      await action()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className={`bg-white rounded-xl border p-5 shadow-sm transition-opacity ${isCompleted ? "opacity-60" : ""} ${loading ? "opacity-50 pointer-events-none" : ""}`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {editing ? (
            <div className="flex flex-col gap-2">
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={2}
                placeholder="Descrição (opcional)"
                className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          ) : (
            <>
              <p className={`text-sm font-medium text-gray-900 ${isCompleted ? "line-through" : ""}`}>
                {task.title}
              </p>
              {task.description && (
                <p className="mt-1 text-sm text-gray-500">{task.description}</p>
              )}
            </>
          )}
        </div>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full ${
            isCompleted ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
          }`}
        >
          {isCompleted ? "concluída" : "pendente"}
        </span>
      </div>

      {error && <p className="mt-2 text-xs text-red-500">{error}</p>}

      <div className="mt-4 flex items-center gap-2">
        {editing ? (
          <>
            <button
              onClick={handleSave}
              disabled={!title.trim()}
              className="text-xs font-medium bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white px-3 py-1.5 rounded-lg transition-colors"
            >
              Salvar
            </button>
            <button
              onClick={handleCancel}
              className="text-xs font-medium text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
            >
              Cancelar
            </button>
          </>
        ) : (
          <>
            {!isCompleted && (
              <button
                onClick={() => handle(() => onComplete(task.id))}
                className="text-xs font-medium text-green-600 hover:text-green-800 px-3 py-1.5 rounded-lg border border-green-200 hover:border-green-400 transition-colors"
              >
                Concluir
              </button>
            )}
            <button
              onClick={() => setEditing(true)}
              disabled={isCompleted}
              className="text-xs font-medium text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg border border-gray-200 hover:border-gray-300 disabled:opacity-40 transition-colors"
            >
              Editar
            </button>
            <button
              onClick={() => handle(() => onDelete(task.id))}
              className="ml-auto text-xs font-medium text-red-500 hover:text-red-700 px-3 py-1.5 rounded-lg border border-red-200 hover:border-red-400 transition-colors"
            >
              Excluir
            </button>
          </>
        )}
      </div>
    </div>
  )
}
