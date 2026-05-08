import { useNavigate } from 'react-router-dom'

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-agri-50 flex flex-col items-center justify-center px-4 text-center">
      <div className="text-6xl mb-6">🌱</div>
      <h1 className="text-4xl md:text-5xl font-bold text-agri-600 mb-3">
        Organic Farming
      </h1>
      <p className="text-gray-500 text-lg mb-8 max-w-md">
        Bienvenue sur votre plateforme de gestion agricole. Suivez vos parcelles,
        cultures, observations et alertes en temps réel.
      </p>
      <button
        onClick={() => navigate('/dashboard')}
        className="bg-agri-500 hover:bg-agri-600 text-white text-lg font-semibold px-8 py-3 rounded-lg transition"
      >
        Accéder à l'application
      </button>
      <p className="text-xs text-gray-400 mt-10">Projet B2 · Sup de Vinci</p>
    </div>
  )
}
