import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Plots from './pages/Plots'
import Crops from './pages/Crops'
import Observations from './pages/Observations'
import Alerts from './pages/Alerts'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="plots" element={<Plots />} />
        <Route path="crops" element={<Crops />} />
        <Route path="observations" element={<Observations />} />
        <Route path="alerts" element={<Alerts />} />
      </Route>
    </Routes>
  )
}
