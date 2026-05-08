import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Plots from './pages/Plots'
import Crops from './pages/Crops'
import Observations from './pages/Observations'
import Alerts from './pages/Alerts'
import ErrorBoundary from './components/ErrorBoundary'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<ErrorBoundary><Dashboard /></ErrorBoundary>} />
        <Route path="plots" element={<ErrorBoundary><Plots /></ErrorBoundary>} />
        <Route path="crops" element={<ErrorBoundary><Crops /></ErrorBoundary>} />
        <Route path="observations" element={<ErrorBoundary><Observations /></ErrorBoundary>} />
        <Route path="alerts" element={<ErrorBoundary><Alerts /></ErrorBoundary>} />
      </Route>
    </Routes>
  )
}
