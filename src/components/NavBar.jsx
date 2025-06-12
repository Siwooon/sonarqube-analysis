import React from 'react'
import { NavLink } from 'react-router-dom'

export default function NavBar() {
  return (
    <nav className="navbar">
      <NavLink to="/users" className={({isActive})=>isActive?'active':''}>Utilisateurs</NavLink>
      <NavLink to="/ressources" className={({isActive})=>isActive?'active':''}>Ressources</NavLink>
      <NavLink to="/emprunts" className={({isActive})=>isActive?'active':''}>Emprunts</NavLink>
    </nav>
)
}
