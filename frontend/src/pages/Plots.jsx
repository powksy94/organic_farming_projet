import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Plots() {
  const [plots, setPlots]   = useState([])
  const [error, setError]   = useState(null)
  const [form, setForm]     = useState({ name: '', location: '', area_ha: '' })
  const [showForm, setShow] = useState(false)

  const load = () => api.plots().then(p => setPlots(Array.isArray(p) ? p : [])).catch(e => setError(e.message))
  useEffect(load, [])

  const submit = async (e) => {
    e.preventDefault()
    try {
      await api.createPlot({
        name: form.name,
        location: form.location,
        area_ha: parseFloat(form.area_ha),
      })
      setForm({ name: '', location: '', area_ha: '' })
      setShow(false)
      load()
    } catch (e) { setError(e.message) }
  }

  const remove = async (id) => {
    if (!confirm('Supprimer cette parcelle ?')) return
    try { await api.deletePlot(id); load() } catch (e) { setError(e.message) }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Parcelles</h1>
        <button onClick={() => setShow(!showForm)}
                className="bg-agri-500 text-white px-4 py-2 rounded hover:bg-agri-600">
          {showForm ? 'Annuler' : '+ Nouvelle parcelle'}
        </button>
      </div>

      {error && <div className="bg-red-50 text-red-700 p-3 rounded mb-3 text-sm">{error}</div>}

      {showForm && (
        <form onSubmit={submit} className="bg-white p-4 rounded shadow-sm mb-4 grid md:grid-cols-3 gap-3">
          <input className="border rounded px-3 py-2" placeholder="Nom"
                 value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
          <input className="border rounded px-3 py-2" placeholder="Localisation"
                 value={form.location} onChange={e => setForm({...form, location: e.target.value})} required />
          <input className="border rounded px-3 py-2" placeholder="Surface (ha)" type="number" step="0.01"
                 value={form.area_ha} onChange={e => setForm({...form, area_ha: e.target.value})} required />
          <div className="md:col-span-3">
            <button className="bg-agri-500 text-white px-4 py-2 rounded">Enregistrer</button>
          </div>
        </form>
      )}

      <div className="bg-white rounded shadow-sm overflow-x-auto">
        <table className="w-full text-sm min-w-[520px]">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-2">#</th>
              <th className="px-4 py-2">Nom</th>
              <th className="px-4 py-2">Localisation</th>
              <th className="px-4 py-2">Surface</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {plots.map(p => (
              <tr key={p.id} className="border-t hover:bg-agri-50">
                <td className="px-4 py-2 text-gray-400">{p.id}</td>
                <td className="px-4 py-2 font-medium">{p.name}</td>
                <td className="px-4 py-2">{p.location}</td>
                <td className="px-4 py-2">{p.area_ha} ha</td>
                <td className="px-4 py-2 text-right">
                  <button onClick={() => remove(p.id)}
                          className="text-red-600 hover:underline text-xs">Supprimer</button>
                </td>
              </tr>
            ))}
            {plots.length === 0 && (
              <tr><td colSpan="5" className="text-center text-gray-400 py-6">Aucune parcelle.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
