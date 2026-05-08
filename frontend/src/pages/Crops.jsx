import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Crops() {
  const [crops, setCrops] = useState([])
  const [plots, setPlots] = useState([])
  const [error, setError] = useState(null)
  const [form, setForm] = useState({ type: '', planting_date: '', plot_id: '' })
  const [showForm, setShow] = useState(false)

  const load = () => {
    Promise.all([api.crops(), api.plots()])
      .then(([c, p]) => { setCrops(Array.isArray(c) ? c : []); setPlots(Array.isArray(p) ? p : []) })
      .catch(e => setError(e.message))
  }
  useEffect(load, [])

  const submit = async (e) => {
    e.preventDefault()
    try {
      await api.createCrop({
        type: form.type,
        planting_date: form.planting_date,
        plot_id: parseInt(form.plot_id),
      })
      setForm({ type: '', planting_date: '', plot_id: '' })
      setShow(false)
      load()
    } catch (e) { setError(e.message) }
  }

  const remove = async (id) => {
    if (!confirm('Supprimer cette culture ?')) return
    try { await api.deleteCrop(id); load() } catch (e) { setError(e.message) }
  }

  const plotName = (id) => plots.find(p => p.id === id)?.name || `#${id}`

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Cultures</h1>
        <button onClick={() => setShow(!showForm)}
                className="bg-agri-500 text-white px-4 py-2 rounded hover:bg-agri-600">
          {showForm ? 'Annuler' : '+ Nouvelle culture'}
        </button>
      </div>

      {error && <div className="bg-red-50 text-red-700 p-3 rounded mb-3 text-sm">{error}</div>}

      {showForm && (
        <form onSubmit={submit} className="bg-white p-4 rounded shadow-sm mb-4 grid md:grid-cols-3 gap-3">
          <input className="border rounded px-3 py-2" placeholder="Type (Blé, Maïs…)"
                 value={form.type} onChange={e => setForm({...form, type: e.target.value})} required />
          <input className="border rounded px-3 py-2" type="date"
                 value={form.planting_date} onChange={e => setForm({...form, planting_date: e.target.value})} required />
          <select className="border rounded px-3 py-2"
                  value={form.plot_id} onChange={e => setForm({...form, plot_id: e.target.value})} required>
            <option value="">— parcelle —</option>
            {plots.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
          <div className="md:col-span-3">
            <button className="bg-agri-500 text-white px-4 py-2 rounded">Enregistrer</button>
          </div>
        </form>
      )}

      <div className="bg-white rounded shadow-sm overflow-x-auto">
        <table className="w-full text-sm min-w-[500px]">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Date semis</th>
              <th className="px-4 py-2">Parcelle</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {crops.map(c => (
              <tr key={c.id} className="border-t hover:bg-agri-50">
                <td className="px-4 py-2 font-medium">{c.type}</td>
                <td className="px-4 py-2">{c.planting_date}</td>
                <td className="px-4 py-2">{plotName(c.plot_id)}</td>
                <td className="px-4 py-2 text-right">
                  <button onClick={() => remove(c.id)}
                          className="text-red-600 hover:underline text-xs">Supprimer</button>
                </td>
              </tr>
            ))}
            {crops.length === 0 && (
              <tr><td colSpan="4" className="text-center text-gray-400 py-6">Aucune culture.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
