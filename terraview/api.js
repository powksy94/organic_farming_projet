// TerraView — connecteur API FastAPI
// Branche le site sur le back de Powksy à la place des données mockées.

const API_BASE = window.API_BASE || 'http://localhost:8000/api';

// Coords des polygones SVG (statiques — pas en BDD)
// Indexées par nom de parcelle pour matcher avec ce que renvoie /api/plots/
window.TV_PARCEL_COORDS = {
  "Le Grand Champ":   { coords: "M 60 80 L 220 70 L 240 180 L 80 200 Z",     labelXY: [148, 138], stade: "Montaison" },
  "Vigne du Coteau":  { coords: "M 280 60 L 420 90 L 410 200 L 270 180 Z",   labelXY: [345, 130], stade: "Floraison" },
  "Maïs Sud":         { coords: "M 80 230 L 300 220 L 320 360 L 70 370 Z",   labelXY: [195, 295], stade: "Levée" },
  "Verger Est":       { coords: "M 340 220 L 460 230 L 450 340 L 330 350 Z", labelXY: [395, 285], stade: "Nouaison" },
  "Prairie Nord":     { coords: "M 470 70 L 600 80 L 595 200 L 460 195 Z",   labelXY: [530, 138], stade: "Repousse" },
  "Tournesol Ouest":  { coords: "M 60 400 L 220 390 L 230 510 L 70 520 Z",   labelXY: [145, 455], stade: "Boutonnage" },
  "Colza Plateau":    { coords: "M 250 380 L 400 390 L 410 510 L 240 510 Z", labelXY: [325, 445], stade: "Maturation" },
  "Orge du Pré":      { coords: "M 430 380 L 600 390 L 595 510 L 430 510 Z", labelXY: [515, 445], stade: "Épiaison" },
  "Verger Sud":       { coords: "M 480 220 L 600 230 L 595 350 L 470 350 Z", labelXY: [535, 285], stade: "Floraison" },
  "Pommes de Terre":  { coords: "M 620 80 L 760 90 L 750 220 L 615 210 Z",   labelXY: [688, 145], stade: "Tubérisation" },
};

// Mapping niveau → sévérité TerraView
const SEVERITE_MAP = { 1: "basse", 2: "moyenne", 3: "haute" };

// Helper fetch
async function jsonFetch(path, opts = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  if (res.status === 204) return null;
  return res.json();
}

// Format date "dd/mm" pour affichage TerraView
function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' });
}

window.TV_API = {

  // -------- LOAD --------
  async loadAll() {
    const [plots, crops, observations, alerts, weather] = await Promise.all([
      jsonFetch('/plots/').catch(()  => []),
      jsonFetch('/crops/').catch(()  => []),
      jsonFetch('/observations/').catch(() => []),
      jsonFetch('/alerts/').catch(() => []),
      jsonFetch('/weather/').catch(() => []),
    ]);

    // Météo la plus récente (pour humidité/température affichées)
    const lastWeather = weather.length
      ? weather.sort((a, b) => b.date.localeCompare(a.date))[0]
      : null;

    // Transformation plots → parcelles TerraView
    const parcelles = plots.map(p => {
      const meta = TV_PARCEL_COORDS[p.name] || {};
      const culture = crops.find(c => c.plot_id === p.id);
      const plotObs = observations
        .filter(o => o.plot_id === p.id)
        .sort((a, b) => b.date.localeCompare(a.date));
      const lastObs = plotObs[0];
      const plotAlerts = alerts.filter(a => a.plot_id === p.id && !a.resolved);

      let statut = "sain";
      if (plotAlerts.some(a => a.level === 3)) statut = "alerte";
      else if (plotAlerts.length > 0) statut = "attention";

      return {
        id: `p${p.id}`,
        _api_id: p.id,
        nom: p.name,
        culture: culture ? culture.type : "—",
        surface: p.area_ha,
        statut,
        humidite:    lastWeather ? Math.round(lastWeather.humidity) : 0,
        temperature: lastWeather ? Math.round(lastWeather.temperature) : 0,
        risque: Math.min(100, plotAlerts.reduce((s, a) => s + a.level * 25, 0)),
        stade: meta.stade || "—",
        derniere_obs: lastObs ? fmtDate(lastObs.date) : "aucune",
        coords: meta.coords || "M 0 0 L 100 0 L 100 100 L 0 100 Z",
        labelXY: meta.labelXY || [50, 50],
      };
    });

    // Transformation alertes
    const alertesFmt = alerts.map(a => {
      const plot = plots.find(p => p.id === a.plot_id);
      return {
        id: `a${a.id}`,
        _api_id: a.id,
        date: fmtDate(a.date),
        parcelle: plot ? plot.name : `Parcelle #${a.plot_id}`,
        type: a.type,
        severite: SEVERITE_MAP[a.level] || "moyenne",
        statut: a.resolved ? "traité" : "nouveau",
        message: a.type,
        action: a.level === 3 ? "Action urgente requise"
              : a.level === 2 ? "Surveillance recommandée"
              : "Suivre l'évolution",
      };
    });

    // Transformation observations
    const obsFmt = observations.map(o => {
      const plot = plots.find(p => p.id === o.plot_id);
      return {
        id: `o${o.id}`,
        _api_id: o.id,
        date: fmtDate(o.date),
        parcelle: plot ? plot.name : `Parcelle #${o.plot_id}`,
        type: o.state,
        notes: o.comment || "",
        auteur: "Léa M.",
      };
    });

    return {
      parcelles,
      alertes: alertesFmt,
      observations: obsFmt,
    };
  },

  // -------- ACTIONS --------
  async resolveAlert(apiId) {
    return jsonFetch(`/alerts/${apiId}/resolve`, { method: 'PUT' });
  },

  async createObservation(data) {
    // data = { date, state, plot_id, comment }
    return jsonFetch('/observations/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async createPlot(data) {
    // data = { name, location, area_ha }
    return jsonFetch('/plots/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async updatePlot(apiId, data) {
    return jsonFetch(`/plots/${apiId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async deletePlot(apiId) {
    return jsonFetch(`/plots/${apiId}`, { method: 'DELETE' });
  },

  async generateAlerts() {
    return jsonFetch('/alerts/generate', { method: 'POST' });
  },
};
