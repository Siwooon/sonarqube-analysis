import React, { useEffect, useState } from 'react'
import { fetchResources, createResource, deleteResource } from '../api.js'

export default function ResourceList() {
  const [resources, setResources] = useState([])
  const [form, setForm] = useState({ titre: '', type: 'Livre', auteur: '' })
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)

  const load = async () => {
    try {
      setError(null)
      const data = await fetchResources({ skip: 0, limit: 100 })
      setResources(data)
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
        await createResource(form)
      }
      setForm({ titre: '', type: 'Livre', auteur: '' })
      setEditing(null)
      setShowForm(false)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const onDelete = async id => {
    try {
      await deleteResource(id)
      load()
    } catch (err) {
      setError(err.message)
    }
  }

  const onEdit = r => {
    setForm({ titre: r.titre, type: r.type, auteur: r.auteur })
    setEditing(r.id)
    setShowForm(true)
  }

  return (
    <div className="container card">
      <h2>Ressources</h2>
      {error && <div className="error-popup">{error}</div>}
      <button className="btn" onClick={() => { setShowForm(!showForm); setEditing(null) }}>
        {showForm ? 'Annuler' : 'Créer une ressource'}
      </button>
      {showForm && (
        <form className="form" onSubmit={onSubmit}>
          <div className="form-group">
            <label>Titre</label>
            <input name="titre" value={form.titre} onChange={onChange} />
          </div>
          <div className="form-group">
            <label>Type</label>
            <select name="type" value={form.type} onChange={onChange}>
              <option>Livre</option>
              <option>Film</option>
              <option>Jeu</option>
              <option>Autre</option>
            </select>
          </div>
          <div className="form-group">
            <label>Auteur</label>
            <input name="auteur" value={form.auteur} onChange={onChange} />
          </div>
          <button className="btn primary" type="submit">{editing ? 'Modifier' : 'Créer'}</button>
        </form>
      )}
      <table className="table">
        <thead><tr><th>Titre</th><th>Type</th><th>Dispo</th><th>Action</th></tr></thead>
        <tbody>
          {resources.map(r => (
            <tr key={r.id} className={r.disponible ? 'available' : 'unavailable'}>
              <td>{r.titre}</td>
              <td>{r.type}</td>
              <td>{r.disponible ? '✔' : '✖'}</td>
              <td>
                <button className="btn small" onClick={() => onEdit(r)}>Modifier</button>
                <button className="btn small danger" onClick={() => onDelete(r.id)}>Supprimer</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
