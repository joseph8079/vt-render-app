import React, { useEffect, useState } from "react";
import { api } from "../app/api";
import { Link } from "react-router-dom";

export default function Patients() {
  const [q, setQ] = useState("");
  const [items, setItems] = useState([]);

  async function load() {
    const res = await api.get("/patients/", { params: q ? { q } : {} });
    setItems(res.data.results || res.data);
  }

  useEffect(() => { load(); }, []);

  return (
    <div>
      <h1 style={{ fontSize: 22 }}>Patients</h1>
      <div className="row">
        <div style={{ flex: 2, minWidth: 260 }}>
          <label>Search</label>
          <input className="input" value={q} onChange={e => setQ(e.target.value)} placeholder="MRN, name..." />
        </div>
        <div style={{ alignSelf: "flex-end" }}>
          <button className="btn" onClick={load}>Search</button>
        </div>
      </div>

      <div style={{ height: 12 }} />
      <div className="card">
        <table>
          <thead><tr><th>Name</th><th>MRN</th><th>Gender</th><th>Location</th><th></th></tr></thead>
          <tbody>
            {items.map(p => (
              <tr key={p.id}>
                <td>{p.last_name}, {p.first_name}</td>
                <td><span className="badge">{p.mrn}</span></td>
                <td>{p.gender}</td>
                <td>{p.location?.name || "-"}</td>
                <td><Link className="btn" to={`/patients/${p.id}`}>Open</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
        {!items.length && <div style={{ opacity: 0.8, padding: 10 }}>No patients found.</div>}
      </div>
    </div>
  );
}
