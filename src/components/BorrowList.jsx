import React, { useEffect, useState } from 'react'
import { fetchBorrows, createBorrow, returnBorrow, fetchUsers, fetchResources } from '../api.js'

export default function BorrowList() {
  const [borrows, setBorrows] = useState([])
  const [users, setUsers] = useState([])
  const [resources, setResources] = useState([])
  const [form, setForm] = useState({ user_id: '', ressource_id: '', date_emprunt: '', date_retour: '' })
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)

  const load = async () => {
    try {
      setError(null)
      const [b, u, r] = await Promise.all([fetchBorrows(), fetchUsers(), fetchResources({ skip:0, limit:100 })])
      setBorrows(b)
      setUsers(u)
      setResources(r)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => { load() }, [])

  const onChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const onSubmit = async e => {
    e.preventDefault()
    try {
      if (editing) {
        alert('Modification non implémentée')
      } else {
        await createBorrow(form)
      }
      setForm({ user_id:'', ressource_id:'', date_emprunt:'', date_retour:'' })
      setEditing(null)
      setShowForm(false)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const onReturn = async id => {
    try {
      await returnBorrow(id)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const onEdit = b => {
    setForm({ user_id:b.user_id, ressource_id:b.ressource_id, date_emprunt:b.date_emprunt, date_retour:b.date_retour })
    setEditing(b.id)
    setShowForm(true)
  }

  return (
    <div className="container card">
      <h2>Emprunts</h2>
      {error && <div className="error-popup">{error}</div>}
      <button className="btn" onClick={() => { setShowForm(!showForm); setEditing(null) }}>
        {showForm ? 'Annuler' : 'Créer un emprunt'}
      </button>
      {showForm && (
        <form className="form" onSubmit={onSubmit}>
          <div className="form-group">
            <label>Utilisateur</label>
            <select name="user_id" value={form.user_id} onChange={onChange}>
              <option value="">--Choisir--</option>
              {users.map(u => <option key={u.id} value={u.id}>{u.nom} {u.prenom}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Ressource</label>
            <select name="ressource_id" value={form.ressource_id} onChange={onChange}>
              <option value="">--Choisir--</option>
              {resources.filter(r => r.disponible).map(r => <option key={r.id} value={r.id}>{r.titre}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Date emprunt</label>
            <input type="date" name="date_emprunt" value={form.date_emprunt} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>Date retour</label>
            <input type="date" name="date_retour" value={form.date_retour} onChange={onChange} />
          </div>
          <button className="btn primary" type="submit">{editing ? 'Modifier' : 'Créer'}</button>
        </form>
      )}
      <table className="table">
        <thead><tr><th>Utilisateur</th><th>Ressource</th><th>Emprunt</th><th>Retour</th><th>Action</th></tr></thead>
        <tbody>
          {borrows.map(b => (
            <tr key={b.id}>
              <td>{users.find(u=>u.id===b.user_id)?.nom || ''}</td>
              <td>{resources.find(r=>r.id===b.ressource_id)?.titre || ''}</td>
              <td>{b.date_emprunt}</td>
              <td>{b.date_retour}</td>
              <td>
                <button className="btn small" onClick={() => onEdit(b)}>Modifier</button>
                <button className="btn small danger" onClick={() => onReturn(b.id)}>Rendre</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
