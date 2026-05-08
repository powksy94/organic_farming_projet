import { useEffect, useState } from 'react'
import { api } from '../api'

const levelColor = (n) => ({1:'bg-blue-100 text-blue-700', 2:'bg-amber-100 text-amber-700', 3:'bg-red-100 text-red-700'}[n] || 'bg-gray-100')
const levelLabel = (n) => ({1:'Faible', 2:'Modéré', 3:'Élevé'}[n] || '?')

export default function Alerts() {
  const [alerts, setAlerts]   = useState([])
  const [plots, setPlots]     = useState([])
  const [error, setError]     = useState(null)
  const [filter, setFilter]   = useState('active')

  const load = () => {
    const params = filter === 'active'   ? { resolved: false }
                  : filter === 'resolved' ? { resolved: true }
                  : {}
    return Promise.all([api.alerts(params), api.plots()])
      .then(([a, p]) => { setAlerts(Array.isArray(a) ? a : []); setPlots(Array.isArray(p) ? p : []) })
      .catch(e => setError(e.message))
  }
  useEffect(load, [filter])

  const resolve = async (id) => {
    try { await api.resolveAlert(id); load() } catch (e) { setError(e.message) }
  }

  const generate = async () => {
    try { await api.generateAlerts(); load() } catch (e) { setError(e.message) }
  }

  const plotName = (id) => plots.find(p => p.id === id)?.name || `#${id}`

  return (
    <div>
      <div className="flex justify-between items-center mb-4 flex-wrap gap-2">
        <h1 className="text-2xl font-bold">Alertes</h1>
        <button onClick={generate}
                className="bg-agri-500 text-white px-4 py-2 rounded hover:bg-agri-600 text-sm">
          ⚡ Générer alertes auto
        </button>
      </div>

      <div className="flex gap-2 mb-4">
        {[
          { v: 'active', l: 'Actives' },
          { v: 'resolved', l: 'Résolues' },
          { v: 'all', l: 'Toutes' },
        ].map(f => (
          <button key={f.v} onClick={() => setFilter(f.v)}
                  className={`px-3 py-1 rounded text-sm ${
                    filter === f.v ? 'bg-agri-500 text-white' : 'bg-white border'
                  }`}>{f.l}</button>
        ))}
      </div>

      {error && <div className="bg-red-50 text-red-700 p-3 rounded mb-3 text-sm">{error}</div>}

      <div className="bg-white rounded shadow-sm overflow-x-auto">
        <table className="w-full text-sm min-w-[560px]">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-2">Date</th>
              <th className="px-4 py-2">Parcelle</th>
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Niveau</th>
              <th className="px-4 py-2">Statut</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {alerts.map(a => (
              <tr key={a.id} className="border-t hover:bg-agri-50">
                <td className="px-4 py-2">{a.date}</td>
                <td className="px-4 py-2">{plotName(a.plot_id)}</td>
                <td className="px-4 py-2">{a.type}</td>
                <td className="px-4 py-2">
                  <span className={`px-2 py-0.5 rounded text-xs ${levelColor(a.level)}`}>
                    {levelLabel(a.level)}
                  </span>
                </td>
                <td className="px-4 py-2">
                  {a.resolved
                    ? <span className="text-green-600 text-xs">✓ Résolue</span>
                    : <span className="text-amber-600 text-xs">⚠ Active</span>}
                </td>
                <td className="px-4 py-2 text-right">
                  {!a.resolved && (
                    <button onClick={() => resolve(a.id)}
                            className="text-agri-500 hover:underline text-xs">Marquer résolue</button>
                  )}
                </td>
              </tr>
            ))}
            {alerts.length === 0 && (
              <tr><td colSpan="6" className="text-center text-gray-400 py-6">Aucune alerte.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
