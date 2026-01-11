import React, { useEffect, useState } from "react";
import { api } from "../app/api";

function Stat({ title, value }) {
  return (
    <div className="card" style={{ flex: 1, minWidth: 220 }}>
      <div style={{ opacity: 0.85, fontSize: 12 }}>{title}</div>
      <div style={{ fontSize: 28, marginTop: 6 }}>{value ?? "-"}</div>
    </div>
  );
}

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    (async () => {
      const res = await api.get("/dashboard/");
      setData(res.data);
    })();
  }, []);

  return (
    <div>
      <h1 style={{ fontSize: 22 }}>Dashboard</h1>
      <div className="row">
        <Stat title="Referrals (last 30 days)" value={data?.referrals_last_30_days} />
        <Stat title="Active Programs" value={data?.active_programs} />
        <Stat title="Upcoming Scheduled Sessions (next 7 days)" value={data?.upcoming_scheduled_sessions_next_7_days} />
      </div>

      <div style={{ height: 12 }} />
      <div className="grid2">
        <div className="card">
          <h2 style={{ fontSize: 16 }}>Funnel</h2>
          <table>
            <thead><tr><th>Status</th><th>Count</th></tr></thead>
            <tbody>
              {data?.funnel && Object.entries(data.funnel).map(([k, v]) => (
                <tr key={k}>
                  <td><span className="badge">{k}</span></td>
                  <td>{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h2 style={{ fontSize: 16 }}>Outcomes (Completed sessions, last 30 days)</h2>
          <div style={{ opacity: 0.9, lineHeight: 1.8 }}>
            Avg symptom score: <b>{fmt(data?.outcomes_last_30_days?.avg_symptom)}</b><br />
            Avg engagement: <b>{fmt(data?.outcomes_last_30_days?.avg_engagement)}</b><br />
            Avg homework compliance: <b>{fmt(data?.outcomes_last_30_days?.avg_homework)}</b>
          </div>

          <div style={{ height: 12 }} />
          <h3 style={{ fontSize: 14 }}>At-risk (next 7 days: fewer than 2 scheduled sessions)</h3>
          <div style={{ opacity: 0.85, fontSize: 13 }}>
            {data?.at_risk_programs_next_7_days?.length
              ? data.at_risk_programs_next_7_days.map(p => (
                <span key={p.id} className="badge" style={{ marginRight: 6, marginBottom: 6 }}>
                  Program #{p.id} (s7={p.s7})
                </span>
              ))
              : <span className="badge">None</span>
            }
          </div>
        </div>
      </div>
    </div>
  );
}

function fmt(v) {
  if (v === null || v === undefined) return "-";
  return Math.round(v * 10) / 10;
}
