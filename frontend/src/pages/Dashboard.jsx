import { useEffect, useState } from 'react'
import { api } from '../api'

function KPI({ label, value, sub, color = 'agri' }) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border-l-4 border-${color}-500 p-4`}>
      <div className="text-xs text-gray-500 uppercase">{label}</div>
      <div className="text-3xl font-bold mt-1">{value}</div>
      {sub && <div className="text-xs text-gray-500 mt-1">{sub}</div>}
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    api.dashboard()
      .then(setData)
      .catch(e => setError(e.message))
  }, [])

  if (error) return (
    <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded">
      Erreur API : {error}
      <div className="text-xs mt-2">Vérifie que le back FastAPI tourne sur http://localhost:8000</div>
    </div>
  )
  if (!data) return <div className="text-gray-400">Chargement…</div>

  const w = data.latest_weather

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Tableau de bord</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <KPI label="Parcelles"
             value={data.plots?.total ?? 0}
             sub={`${data.plots?.total_area_ha ?? 0} ha`} />
        <KPI label="Alertes actives"
             value={data.alerts?.active ?? 0}
             sub={`${data.alerts?.critical ?? 0} critiques`}
             color="amber" />
        <KPI label="Cultures"
             value={Object.values(data.crops || {}).reduce((a, b) => a + b, 0)}
             sub={`${Object.keys(data.crops || {}).length} types`}
             color="blue" />
        {w && (
          <KPI label="Météo"
               value={`${w.temperature}°C`}
               sub={`Hum. ${w.humidity}% · Pluie ${w.rain_mm}mm`}
               color="sky" />
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <h2 className="font-semibold mb-3">Cultures par type</h2>
          {Object.entries(data.crops || {}).length === 0 ? (
            <p className="text-gray-400 text-sm">Aucune culture.</p>
          ) : (
            <ul className="space-y-1 text-sm">
              {Object.entries(data.crops).map(([type, n]) => (
                <li key={type} className="flex justify-between">
                  <span>{type}</span>
                  <span className="font-semibold">{n}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm p-4">
          <h2 className="font-semibold mb-3">Observations récentes</h2>
          {(!data.observations?.recent || data.observations.recent.length === 0) ? (
            <p className="text-gray-400 text-sm">Aucune observation récente.</p>
          ) : (
            <ul className="space-y-2 text-sm">
              {data.observations.recent.map(o => (
                <li key={o.id} className="border-b pb-1 last:border-0">
                  <div className="flex justify-between">
                    <span className="font-medium">{o.state}</span>
                    <span className="text-gray-400">{o.date}</span>
                  </div>
                  {o.comment && <div className="text-xs text-gray-500">{o.comment}</div>}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
