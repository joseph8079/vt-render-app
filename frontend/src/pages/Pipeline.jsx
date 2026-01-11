import React, { useEffect, useMemo, useState } from "react";
import { api } from "../app/api";

const STATUSES = [
  "FLAGGED","INTAKE_CREATED","REVIEW_PENDING","REVIEW_COMPLETED","PLAN_READY",
  "PARENT_CONTACTED","PARENT_CONFIRMED","SLOT_ASSIGNED","SCHEDULED_INTERNAL",
  "ACTIVE_THERAPY","ON_HOLD","COMPLETED","DROPPED"
];

export default function Pipeline() {
  const [items, setItems] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [q, setQ] = useState("");

  async function load() {
    const res = await api.get("/referrals/");
    setItems(res.data.results || res.data);
  }

  useEffect(() => { load(); }, []);

  const filtered = useMemo(() => {
    let x = items;
    if (statusFilter) x = x.filter(r => r.status === statusFilter);
    if (q) x = x.filter(r => (`${r.patient?.mrn} ${r.patient?.first_name} ${r.patient?.last_name}`).toLowerCase().includes(q.toLowerCase()));
    return x;
  }, [items, statusFilter, q]);

  return (
    <div>
      <h1 style={{ fontSize: 22 }}>Pipeline</h1>

      <div className="row">
        <div style={{ flex: 2, minWidth: 260 }}>
          <label>Search</label>
          <input className="input" value={q} onChange={e => setQ(e.target.value)} placeholder="MRN, name..." />
        </div>
        <div style={{ flex: 1, minWidth: 220 }}>
          <label>Status</label>
          <select className="input" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
            <option value="">All</option>
            {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div style={{ alignSelf: "flex-end" }}>
          <button className="btn" onClick={load}>Refresh</button>
        </div>
      </div>

      <div style={{ height: 12 }} />
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Patient</th><th>MRN</th><th>Location</th><th>Status</th><th>Updated</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(r => (
              <tr key={r.id}>
                <td>{r.patient?.last_name}, {r.patient?.first_name}</td>
                <td><span className="badge">{r.patient?.mrn}</span></td>
                <td>{r.patient?.location?.name || "-"}</td>
                <td><span className="badge">{r.status}</span></td>
                <td>{new Date(r.updated_at).toLocaleString()}</td>
                <td><StatusActions referral={r} onChanged={load} /></td>
              </tr>
            ))}
          </tbody>
        </table>
        {!filtered.length && <div style={{ opacity: 0.8, padding: 10 }}>No referrals.</div>}
      </div>
    </div>
  );
}

function StatusActions({ referral, onChanged }) {
  const [next, setNext] = useState("");
  const [busy, setBusy] = useState(false);

  return (
    <div className="row" style={{ gap: 8 }}>
      <select className="input" style={{ minWidth: 180 }} value={next} onChange={e => setNext(e.target.value)}>
        <option value="">Move to...</option>
        {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
      </select>
      <button className="btn primary" disabled={!next || busy} onClick={async () => {
        setBusy(true);
        try {
          await api.post(`/referrals/${referral.id}/transition/`, { status: next });
          setNext("");
          onChanged();
        } finally {
          setBusy(false);
        }
      }}>Update</button>
    </div>
  );
}
