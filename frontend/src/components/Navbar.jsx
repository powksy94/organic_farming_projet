import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard',    label: 'Tableau de bord' },
  { to: '/plots',        label: 'Parcelles' },
  { to: '/crops',        label: 'Cultures' },
  { to: '/observations', label: 'Observations' },
  { to: '/alerts',       label: 'Alertes' },
]

export default function Navbar() {
  return (
    <nav className="bg-agri-500 text-white shadow">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between flex-wrap gap-2">
        <div className="font-bold text-xl">🌱 Organic Farming</div>
        <div className="flex gap-1 flex-wrap">
          {links.map(l => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `px-3 py-1.5 rounded text-sm transition ${
                  isActive ? 'bg-agri-600' : 'hover:bg-agri-600/60'
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  )
}
