const BASE = 'http://localhost:8000'

export async function fetchUsers(skip = 0, limit = 100) {
  const res = await fetch(`${BASE}/users?skip=${skip}&limit=${limit}`)
  if (!res.ok) {
    const { detail } = await res.json().catch(() => ({}))
    throw new Error(detail || `Erreur ${res.status}`)
  }
  return res.json()
}

export async function createUser(data) {
  const res = await fetch(`${BASE}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const { detail } = await res.json().catch(() => ({}))
    throw new Error(detail || `Erreur ${res.status}`)
  }
  return res.json()
}

export async function deleteUser(id) {
  const res = await fetch(`${BASE}/users/${id}`, { method: 'DELETE' })
  if (!res.ok) {
    const { detail } = await res.json().catch(() => ({}))
    throw new Error(detail || `Erreur ${res.status}`)
  }
}

export async function fetchResources(params={}) {
  const ps = new URLSearchParams(params)
  const res = await fetch(`${BASE}/ressources?${ps}`)
  return res.json()
}
export async function createResource(data) {
  const res = await fetch(`${BASE}/ressources`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) })
  return res.json()
}
export async function deleteResource(id) { await fetch(`${BASE}/ressources/${id}`, {method:'DELETE'}) }

export async function fetchBorrows(skip=0, limit=100) {
  const res = await fetch(`${BASE}/emprunts?skip=${skip}&limit=${limit}`)
  return res.json()
}
export async function createBorrow(data) {
  const res = await fetch(`${BASE}/emprunts`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) })
  return res.json()
}
export async function returnBorrow(id) { await fetch(`${BASE}/emprunts/${id}`, {method:'DELETE'}) }