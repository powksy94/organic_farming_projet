const BASE = import.meta.env.VITE_API_URL || '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const txt = await res.text().catch(() => '')
    throw new Error(`API ${res.status} : ${txt || res.statusText}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  // Dashboard
  dashboard: () => request('/dashboard/'),

  // Plots
  plots:        () => request('/plots/'),
  plot:         (id) => request(`/plots/${id}`),
  createPlot:   (data) => request('/plots/', { method: 'POST', body: JSON.stringify(data) }),
  updatePlot:   (id, data) => request(`/plots/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deletePlot:   (id) => request(`/plots/${id}`, { method: 'DELETE' }),

  // Crops
  crops:        (plotId) => request(`/crops/${plotId ? `?plot_id=${plotId}` : ''}`),
  createCrop:   (data) => request('/crops/', { method: 'POST', body: JSON.stringify(data) }),
  deleteCrop:   (id) => request(`/crops/${id}`, { method: 'DELETE' }),

  // Observations
  observations:      (plotId) => request(`/observations/${plotId ? `?plot_id=${plotId}` : ''}`),
  createObservation: (data) => request('/observations/', { method: 'POST', body: JSON.stringify(data) }),
  deleteObservation: (id) => request(`/observations/${id}`, { method: 'DELETE' }),

  // Alerts
  alerts:        (params = {}) => {
    const qs = new URLSearchParams(params).toString()
    return request(`/alerts/${qs ? '?' + qs : ''}`)
  },
  resolveAlert:  (id) => request(`/alerts/${id}/resolve`, { method: 'PUT' }),
  generateAlerts: () => request('/alerts/generate', { method: 'POST' }),

  // Weather
  weather: () => request('/weather/'),
}
