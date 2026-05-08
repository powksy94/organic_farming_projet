import { useEffect, useState } from 'react'
import { api } from '../api'

const STATES = ['OK', 'Stress hydrique', 'Risque maladie', 'Maladie détectée']
const stateColor = (s) => ({
  'OK': 'bg-green-100 text-green-700',
  'Stress hydrique': 'bg-amber-100 text-amber-700',
  'Risque maladie': 'bg-amber-100 text-amber-700',
  'Maladie détectée': 'bg-red-100 text-red-700',
}[s] || 'bg-gray-100 text-gray-600')

export default function Observations() {
  const [obs, setObs] = useState([])
  const [plots, setPlots] = useState([])
  const [error, setError] = useState(null)
  const [form, setForm] = useState({
    date: new Date().toISOString().slice(0, 10),
    state: 'OK', plot_id: '', comment: ''
  })
  const [showForm, setShow] = useState(false)

  const load = () => {
    Promise.all([api.observations(), api.plots()])
      .then(([o, p]) => { setObs(Array.isArray(o) ? o : []); setPlots(Array.isArray(p) ? p : []) })
      .catch(e => setError(e.message))
  }
  useEffect(load, [])

  const submit = async (e) => {
    e.preventDefault()
    try {
      await api.createObservation({
        date: form.date,
        state: form.state,
        plot_id: parseInt(form.plot_id),
        comment: form.comment || null,
      })
      setForm({ ...form, plot_id: '', comment: '' })
      setShow(false)
      load()
    } catch (e) { setError(e.message) }
  }

  const remove = async (id) => {
    if (!confirm('Supprimer cette observation ?')) return
    try { await api.deleteObservation(id); load() } catch (e) { setError(e.message) }
  }

  const plotName = (id) => plots.find(p => p.id === id)?.name || `#${id}`

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Observations</h1>
        <button onClick={() => setShow(!showForm)}
                className="bg-agri-500 text-white px-4 py-2 rounded hover:bg-agri-600">
          {showForm ? 'Annuler' : '+ Nouvelle observation'}
        </button>
      </div>

      {error && <div className="bg-red-50 text-red-700 p-3 rounded mb-3 text-sm">{error}</div>}

      {showForm && (
        <form onSubmit={submit} className="bg-white p-4 rounded shadow-sm mb-4 grid md:grid-cols-2 gap-3">
          <input className="border rounded px-3 py-2" type="date"
                 value={form.date} onChange={e => setForm({...form, date: e.target.value})} required />
          <select className="border rounded px-3 py-2"
                  value={form.plot_id} onChange={e => setForm({...form, plot_id: e.target.value})} required>
            <option value="">— parcelle —</option>
            {plots.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
          <select className="border rounded px-3 py-2 md:col-span-2"
                  value={form.state} onChange={e => setForm({...form, state: e.target.value})}>
            {STATES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
          <textarea className="border rounded px-3 py-2 md:col-span-2" rows="3" placeholder="Commentaire (optionnel)"
                    value={form.comment} onChange={e => setForm({...form, comment: e.target.value})} />
          <div className="md:col-span-2">
            <button className="bg-agri-500 text-white px-4 py-2 rounded">Enregistrer</button>
          </div>
        </form>
      )}

      <div className="bg-white rounded shadow-sm overflow-x-auto">
        <table className="w-full text-sm min-w-[580px]">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="px-4 py-2">Date</th>
              <th className="px-4 py-2">Parcelle</th>
              <th className="px-4 py-2">État</th>
              <th className="px-4 py-2">Commentaire</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            {obs.map(o => (
              <tr key={o.id} className="border-t hover:bg-agri-50">
                <td className="px-4 py-2">{o.date}</td>
                <td className="px-4 py-2">{plotName(o.plot_id)}</td>
                <td className="px-4 py-2">
                  <span className={`px-2 py-0.5 rounded text-xs ${stateColor(o.state)}`}>{o.state}</span>
                </td>
                <td className="px-4 py-2 text-gray-500 text-xs">{o.comment || '—'}</td>
                <td className="px-4 py-2 text-right">
                  <button onClick={() => remove(o.id)}
                          className="text-red-600 hover:underline text-xs">Supprimer</button>
                </td>
              </tr>
            ))}
            {obs.length === 0 && (
              <tr><td colSpan="5" className="text-center text-gray-400 py-6">Aucune observation.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
