// TerraView — Mes parcelles + Détail parcelle
const { useState: useStateP } = React;

function ParcelThumb({ parcelle }) {
  const color = StatusColor(parcelle.statut);
  return (
    <div className="parcel-thumb" style={{ background: `linear-gradient(180deg, ${color}11, transparent 90%)` }}>
      <svg viewBox="0 0 280 90" style={{ width: "100%", height: "100%" }}>
        <defs>
          <pattern id={`hatch-${parcelle.id}`} width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="10" stroke={color} strokeWidth="1" opacity="0.18" />
          </pattern>
        </defs>
        <rect width="280" height="90" fill={`url(#hatch-${parcelle.id})`} />
        <path d={`M 30 60 Q 70 30 130 38 T 250 30`} stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
        <path d={`M 30 70 Q 80 50 150 55 T 250 50`} stroke={color} strokeWidth="1.5" fill="none" opacity="0.35" />
      </svg>
      <div style={{ position: "absolute", top: 10, left: 12 }}>
        <span className={"pill " + parcelle.statut}>
          <span className="pdot" /> {StatusLabel(parcelle.statut)}
        </span>
      </div>
    </div>
  );
}

function ParcelCard({ parcelle, onClick }) {
  return (
    <button className="parcel-card" onClick={onClick}>
      <ParcelThumb parcelle={parcelle} />
      <div className="parcel-body">
        <h3 className="parcel-name">{parcelle.nom}</h3>
        <p className="parcel-culture">{parcelle.culture} · {parcelle.surface} ha · {parcelle.stade}</p>
        <div className="parcel-stats">
          <div>
            <div className="parcel-stat-l">Humidité</div>
            <div className="parcel-stat-v" style={{ color: parcelle.humidite < 25 ? "var(--red)" : parcelle.humidite < 35 ? "var(--orange)" : "var(--ink)" }}>{parcelle.humidite}%</div>
          </div>
          <div>
            <div className="parcel-stat-l">T°</div>
            <div className="parcel-stat-v">{parcelle.temperature}°C</div>
          </div>
          <div>
            <div className="parcel-stat-l">Risque</div>
            <div className="parcel-stat-v" style={{ color: parcelle.risque > 50 ? "var(--red)" : parcelle.risque > 30 ? "var(--orange)" : "var(--ink)" }}>{parcelle.risque}%</div>
          </div>
        </div>
      </div>
    </button>
  );
}

function ParcelForm({ parcelle, onClose, onSaved }) {
  const editing = !!parcelle;
  const [form, setForm] = useStateP({
    name:     parcelle?.nom || "",
    location: parcelle?.localisation || "Beaune",
    area_ha:  parcelle?.surface || 1,
  });
  const [busy, setBusy] = useStateP(false);
  const [err, setErr]   = useStateP("");

  async function submit(e) {
    e.preventDefault();
    setBusy(true); setErr("");
    try {
      const data = {
        name: form.name.trim(),
        location: form.location.trim(),
        area_ha: parseFloat(form.area_ha) || 0,
      };
      if (editing) await TV_API.updatePlot(parcelle._api_id, data);
      else         await TV_API.createPlot(data);
      onSaved();
    } catch (e) {
      setErr(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function remove() {
    if (!confirm(`Supprimer la parcelle "${parcelle.nom}" ?`)) return;
    setBusy(true); setErr("");
    try {
      await TV_API.deletePlot(parcelle._api_id);
      onSaved();
    } catch (e) { setErr(e.message); setBusy(false); }
  }

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,.4)", zIndex: 100,
      display: "grid", placeItems: "center", padding: 20
    }} onClick={onClose}>
      <div className="card" style={{ width: 440, maxWidth: "100%" }} onClick={e => e.stopPropagation()}>
        <div className="card-head">
          <h3 className="card-title">{editing ? "Modifier la parcelle" : "Nouvelle parcelle"}</h3>
          <button className="btn ghost" onClick={onClose} type="button">×</button>
        </div>
        <form onSubmit={submit} className="form-grid">
          <div className="form-row">
            <label className="form-label">Nom</label>
            <input className="form-input" required autoFocus
                   value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          </div>
          <div className="form-row split">
            <div className="form-row">
              <label className="form-label">Localisation</label>
              <input className="form-input" required
                     value={form.location} onChange={e => setForm({...form, location: e.target.value})} />
            </div>
            <div className="form-row">
              <label className="form-label">Surface (ha)</label>
              <input className="form-input" type="number" step="0.1" min="0.1" required
                     value={form.area_ha} onChange={e => setForm({...form, area_ha: e.target.value})} />
            </div>
          </div>
          {err && <div style={{ background: "var(--red-soft)", color: "var(--red)", padding: 8, borderRadius: 8, fontSize: 12 }}>{err}</div>}
          <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
            <button type="submit" className="btn" disabled={busy}>
              {busy ? "..." : (editing ? "Enregistrer" : "Créer")}
            </button>
            <button type="button" className="btn ghost" onClick={onClose}>Annuler</button>
            {editing && (
              <button type="button" onClick={remove} disabled={busy}
                      style={{ marginLeft: "auto", background: "transparent", border: 0, color: "var(--red)", fontSize: 12, cursor: "pointer" }}>
                Supprimer
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

function ParcelsScreen({ parcelles, setRoute }) {
  const [filter, setFilter] = useStateP("tous");
  const [editing, setEditing] = useStateP(null);
  const filtered = filter === "tous" ? parcelles : parcelles.filter(p => p.statut === filter);

  function reload() {
    setEditing(null);
    if (window.__TV_RELOAD__) window.__TV_RELOAD__();
  }

  return (
    <div>
      <Topbar title="Mes parcelles" subtitle={`${parcelles.length} parcelles · ${parcelles.reduce((a,p)=>a+p.surface,0).toFixed(1)} ha au total`} />
      <div className="filter-bar">
        <div className="seg">
          <button className={filter==="tous"?"on":""} onClick={()=>setFilter("tous")}>Toutes</button>
          <button className={filter==="sain"?"on":""} onClick={()=>setFilter("sain")}>Saines</button>
          <button className={filter==="attention"?"on":""} onClick={()=>setFilter("attention")}>Attention</button>
          <button className={filter==="alerte"?"on":""} onClick={()=>setFilter("alerte")}>Alertes</button>
        </div>
        <div style={{ marginLeft: "auto" }}>
          <button className="btn" onClick={() => setEditing("new")}>
            <Ic.plus width="14" height="14" /> Ajouter une parcelle
          </button>
        </div>
      </div>
      <div className="parcel-grid">
        {filtered.map((p) => (
          <div key={p.id} style={{ position: "relative" }}>
            <ParcelCard parcelle={p} onClick={() => setRoute({ name: "parcel", id: p.id })} />
            <button onClick={(e) => { e.stopPropagation(); setEditing(p); }}
                    title="Modifier"
                    style={{
                      position: "absolute", top: 10, right: 10,
                      width: 28, height: 28, borderRadius: 6,
                      border: "1px solid var(--line)", background: "var(--bg-elev)",
                      cursor: "pointer", fontSize: 13, display: "grid", placeItems: "center",
                    }}>✎</button>
          </div>
        ))}
        <button className="parcel-card add" onClick={() => setEditing("new")}>
          <Ic.plus width="22" height="22" />
          Ajouter une parcelle
        </button>
      </div>
      {editing && (
        <ParcelForm parcelle={editing === "new" ? null : editing}
                    onClose={() => setEditing(null)}
                    onSaved={reload} />
      )}
    </div>
  );
}

function ParcelDetail({ parcelle, alertes, observations, setRoute }) {
  const Wic = { soleil: Ic.sun, nuage: Ic.cloud, pluie: Ic.rain };
  const parcelAlerts = alertes.filter(a => a.parcelle === parcelle.nom);
  const parcelObs = observations.filter(o => o.parcelle === parcelle.nom);
  const W = 460, H = 160, padL = 28, padR = 8, padT = 10, padB = 22;
  const data = TV_DATA.humidite7j[parcelle.id];
  const xAt = (i) => padL + (i/6)*(W-padL-padR);
  const yAt = (v) => padT + (1 - (v-10)/50)*(H-padT-padB);
  const path = data.map((v,i)=>(i===0?"M":"L")+xAt(i)+" "+yAt(v)).join(" ");
  const area = path + " L " + xAt(6) + " " + (H-padB) + " L " + xAt(0) + " " + (H-padB) + " Z";
  const color = StatusColor(parcelle.statut);

  return (
    <div>
      <Topbar
        title={parcelle.nom}
        subtitle={`${parcelle.culture} · ${parcelle.surface} ha · stade ${parcelle.stade}`}
      />
      <button className="back-btn" onClick={() => setRoute({ name: "parcels" })}>
        <Ic.back width="14" height="14" /> Mes parcelles
      </button>

      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 18 }}>
        <span className={"pill " + parcelle.statut}><span className="pdot" /> {StatusLabel(parcelle.statut)}</span>
        <span className="pill neutral"><span className="pdot" /> Dernière obs. {parcelle.derniere_obs}</span>
      </div>

      <div className="kpi-row">
        <Kpi label="Humidité du sol" value={parcelle.humidite} unit="%" trend="Seuil bas: 25%" trendDir={parcelle.humidite < 25 ? "down" : "neutral"} ic={Ic.drop} tone="var(--blue)" />
        <Kpi label="Température" value={parcelle.temperature} unit="°C" trend="Optimal 18–24" trendDir="neutral" ic={Ic.thermo} tone="var(--orange)" />
        <Kpi label="Risque maladie" value={parcelle.risque} unit="%" trend={parcelle.risque > 50 ? "Surveillance accrue" : "Sous le seuil"} trendDir={parcelle.risque > 50 ? "up" : "neutral"} ic={Ic.bug} tone="var(--red)" />
        <Kpi label="Surface" value={parcelle.surface} unit="ha" trend={parcelle.stade} trendDir="neutral" ic={Ic.leaf} tone="var(--green)" />
      </div>

      <div className="detail-grid">
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div className="card">
            <div className="card-head">
              <div>
                <h3 className="card-title">Humidité du sol — 7 jours</h3>
                <p className="card-sub">Mesures stations capteur · semaine 19</p>
              </div>
            </div>
            <svg viewBox={`0 0 ${W} ${H}`} className="chart-svg" style={{ height: 180 }}>
              {[10,30,50,60].map(v=>(
                <g key={v} className="chart-grid">
                  <line x1={padL} x2={W-padR} y1={yAt(v)} y2={yAt(v)}/>
                  <text className="chart-axis" x={padL-6} y={yAt(v)+3} textAnchor="end">{v}%</text>
                </g>
              ))}
              {["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"].map((d,i)=>(
                <text key={d} className="chart-axis" x={xAt(i)} y={H-6} textAnchor="middle">{d}</text>
              ))}
              <path d={area} fill={color} className="chart-area" />
              <path d={path} stroke={color} className="chart-line" />
              {data.map((v,i)=>(
                <circle key={i} cx={xAt(i)} cy={yAt(v)} r="3" fill={color} stroke="var(--bg-elev)" strokeWidth="1.5" />
              ))}
              {/* threshold */}
              <line x1={padL} x2={W-padR} y1={yAt(25)} y2={yAt(25)} stroke="var(--red)" strokeWidth="1" strokeDasharray="3 3" opacity="0.5" />
              <text x={W-padR-4} y={yAt(25)-3} textAnchor="end" fontSize="9" fill="var(--red)" fontFamily="var(--font-mono)">seuil 25%</text>
            </svg>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">Météo locale — 7 jours</h3>
              <span className="pill info"><span className="pdot" /> Station Beaune-Sud</span>
            </div>
            <div className="weather-row">
              {TV_DATA.meteo7j.map((d) => {
                const Wi = Wic[d.ic];
                return (
                  <div className="wd" key={d.j}>
                    <div className="wd-j">{d.j}</div>
                    <Wi className="wd-ic" width="20" height="20" style={{ color: d.ic==="soleil"?"var(--orange)":d.ic==="pluie"?"var(--blue)":"var(--ink-3)" }} />
                    <div className="wd-t">{d.t}°</div>
                    <div className="wd-p">{d.p > 0 ? `${d.p}mm` : "—"}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div className="card">
            <div className="card-head">
              <h3 className="card-title">Alertes liées</h3>
              <span className="eyebrow">{parcelAlerts.length}</span>
            </div>
            <div className="alert-list">
              {parcelAlerts.length === 0 ? (
                <div style={{ color: "var(--ink-3)", fontSize: 13, padding: "10px 0" }}>Aucune alerte active.</div>
              ) : parcelAlerts.map(a => (
                <div key={a.id} className="alert-row" style={{ gridTemplateColumns: "auto 1fr" }}>
                  <div className={"alert-icon " + a.severite}><Ic.alert width="16" height="16" /></div>
                  <div className="alert-body">
                    <h4 className="a-title">{a.type}</h4>
                    <div className="a-meta">
                      <span>{a.date}</span><span>·</span>
                      <span className={"pill " + (a.statut==="traité"?"neutral":a.severite==="haute"?"alerte":"attention")}>
                        <span className="pdot" /> {a.statut}
                      </span>
                    </div>
                    <p className="a-action">{a.message}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-head">
              <h3 className="card-title">Observations</h3>
              <button className="btn ghost"><Ic.plus width="13" height="13" /> Ajouter</button>
            </div>
            <div className="obs-list">
              {parcelObs.length === 0 ? (
                <div style={{ color: "var(--ink-3)", fontSize: 13, padding: "10px 0" }}>Aucune observation pour cette parcelle.</div>
              ) : parcelObs.map(o => (
                <div key={o.id} className="obs-item" style={{ gridTemplateColumns: "60px 1fr" }}>
                  <div className="obs-date">{o.date.replace(" 2026","")}</div>
                  <div>
                    <h4 className="obs-title">{o.type}</h4>
                    <p className="obs-notes">{o.notes}</p>
                    <div className="obs-meta">— {o.auteur}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

window.ParcelsScreen = ParcelsScreen;
window.ParcelDetail = ParcelDetail;
