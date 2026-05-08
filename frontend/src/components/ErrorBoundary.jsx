import { Component } from 'react'

export default class ErrorBoundary extends Component {
  state = { error: null }

  static getDerivedStateFromError(error) {
    return { error }
  }

  render() {
    if (this.state.error) {
      return (
        <div className="bg-red-50 border border-red-200 text-red-700 p-6 rounded m-4">
          <div className="font-semibold mb-1">Une erreur est survenue sur cette page.</div>
          <div className="text-sm text-red-500">{this.state.error.message}</div>
          <button
            className="mt-3 text-sm underline"
            onClick={() => this.setState({ error: null })}
          >
            Réessayer
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
