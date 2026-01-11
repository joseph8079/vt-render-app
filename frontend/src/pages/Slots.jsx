import React, { useEffect, useState } from "react";
import { api } from "../app/api";

export default function Slots() {
  const [slots, setSlots] = useState([]);

  async function load() {
    const res = await api.get("/slot-templates/");
    setSlots(res.data.results || res.data);
  }

  useEffect(() => { load(); }, []);

  return (
    <div>
      <h1 style={{ fontSize: 22 }}>Slot Templates</h1>

      <div className="card">
        <table>
          <thead><tr><th>Location</th><th>Therapist</th><th>Pair</th><th>Time</th><th>Allowed</th><th>Minutes</th></tr></thead>
          <tbody>
            {slots.map(s => (
              <tr key={s.id}>
                <td>{s.location?.name}</td>
                <td>{s.therapist?.username}</td>
                <td><span className="badge">{s.day1}/{s.day2}</span></td>
                <td><span className="badge">{s.time_start}</span></td>
                <td><span className="badge">{s.patient_gender_allowed}</span></td>
                <td>{s.session_minutes}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!slots.length && <div style={{ opacity: 0.8, padding: 10 }}>No slots yet. Create them in Django Admin or run seed_demo.</div>}
      </div>

      <div style={{ height: 12 }} />
      <div className="card">
        <h2 style={{ fontSize: 16 }}>Admin</h2>
        <p style={{ opacity: 0.85, fontSize: 13, lineHeight: 1.5 }}>
          Full slot CRUD is available in <b>Django Admin</b> (recommended for now).
        </p>
        <a className="btn" href="/admin" target="_blank" rel="noreferrer">Open Admin</a>
      </div>
    </div>
  );
}
