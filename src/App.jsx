import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import NavBar from './components/NavBar.jsx'
import UserList from './components/UserList.jsx'
import ResourceList from './components/ResourceList.jsx'
import BorrowList from './components/BorrowList.jsx'

export default function App() {
  return (
    <Router>
      <NavBar />
      <main>
        <Routes>
          <Route path="/users" element={<UserList />} />
          <Route path="/ressources" element={<ResourceList />} />
          <Route path="/emprunts" element={<BorrowList />} />
          <Route path="*" element={<Navigate to="/users" replace />} />
        </Routes>
      </main>
    </Router>
  )
}