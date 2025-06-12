// src/components/UserList.jsx

import React, { useEffect, useState } from 'react'
import { fetchUsers, createUser, deleteUser } from '../api.js'

export default function UserList() {
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({
    nom: '',
    prenom: '',
    mail: '',
    numero_telephone: '',
    nationalite: '',
  })
  const [error, setError] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)

  // Charge la liste des utilisateurs
  const load = async () => {
    try {
      setError(null)
      const data = await fetchUsers()
      setUsers(data)
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const onChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const onSubmit = async e => {
    e.preventDefault()
    try {
      setError(null)
      if (editing) {
        alert('Modification non implémentée')
      } else {
        await createUser(form)
      }
      setForm({
        nom: '',
        prenom: '',
        mail: '',
        numero_telephone: '',
        nationalite: '',
      })
      setEditing(null)
      setShowForm(false)
      await load()
    } catch (err) {
      setError(err.message)
    }
  }

  const onDelete = async id => {
    try {
      setError(null)
      await deleteUser(id)
      await load()
    } catch (err) {
      // Affiche dans le popup
      setError(err.message)
    }
  }

  const onEdit = u => {
    setForm({
      nom: u.nom,
      prenom: u.prenom,
      mail: u.mail,
      numero_telephone: u.numero_telephone,
      nationalite: u.nationalite,
    })
    setEditing(u.id)
    setShowForm(true)
  }

  return (
    <div className="container card">
      <h2>Utilisateurs</h2>

      {/* Popup d'erreur */}
      {error && (
        <div className="error-popup">
          <span>{error}</span>
          <button
            className="btn small"
            onClick={() => setError(null)}
            aria-label="Fermer le message d'erreur"
          >
            ✕
          </button>
        </div>
      )}

      <button
        className="btn default"
        onClick={() => {
          setShowForm(!showForm)
          setEditing(null)
          setError(null)
        }}
      >
        {showForm ? 'Annuler' : 'Créer un utilisateur'}
      </button>

      {showForm && (
        <form className="form" onSubmit={onSubmit}>
          {['nom', 'prenom', 'mail', 'numero_telephone', 'nationalite'].map(
            field => (
              <div className="form-group" key={field}>
                <label className="form-label" htmlFor={field}>
                  {field}
                </label>
                <input
                  className="form-input"
                  id={field}
                  name={field}
                  value={form[field]}
                  onChange={onChange}
                />
              </div>
            )
          )}
          <button className="btn primary" type="submit">
            {editing ? 'Modifier' : 'Créer'}
          </button>
        </form>
      )}

      <table className="table">
        <thead>
          <tr>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Email</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id}>
              <td>{u.nom}</td>
              <td>{u.prenom}</td>
              <td>{u.mail}</td>
              <td>
                <button className="btn small" onClick={() => onEdit(u)}>
                  Modifier
                </button>
                <button
                  className="btn small danger"
                  onClick={() => onDelete(u.id)}
                >
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
