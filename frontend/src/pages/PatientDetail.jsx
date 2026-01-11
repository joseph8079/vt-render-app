import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../app/api";

export default function PatientDetail() {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const [programs, setPrograms] = useState([]);
  const [program, setProgram] = useState(null);

  const [slots, setSlots] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [slotId, setSlotId] = useState("");

  const [noteText, setNoteText] = useState("");
  const [notes, setNotes] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [templateId, setTemplateId] = useState(null);

  async function load() {
    const p = await api.get(`/patients/${id}/`);
    setPatient(p.data);

    const pr = await api.get("/programs/", { params: { patient: id } });
    const list = pr.data.results || pr.data;
    setPrograms(list);
    setProgram(list[0] || null);

    const t = await api.get("/note-templates/");
    const tlist = t.data.results || t.data;
    setTemplates(tlist);
    const defaultSession = tlist.find(x => x.kind === "SESSION" && x.is_active) || tlist[0];
    setTemplateId(defaultSession?.id || null);

    if (list[0]?.id) {
      const n = await api.get("/notes/by_program", { params: { program_id: list[0].id } });
      setNotes(n.data);
    } else {
      setNotes([]);
    }
  }

  useEffect(() => { load(); }, [id]);

  useEffect(() => {
    if (!patient) return;
    (async () => {
      const params = (patient.gender && patient.gender !== "U") ? { patient_gender: patient.gender } : {};
      const s = await api.get("/slot-templates/", { params });
      setSlots(s.data.results || s.data);
    })();
  }, [patient]);

  async function createProgram() {
    const res = await api.post("/programs/", {
      patient: patient.id,
      total_sessions: 22,
      sessions_per_week: 2,
      session_minutes: 30,
      status: "PLANNED",
      notes: ""
    });
    await load();
    setProgram(res.data);
  }

  async function assignSlot() {
    if (!program?.id) return alert("Create a program first");
    if (!startDate) return alert("Pick a start date");
    if (!slotId) return alert("Pick a slot");
    await api.post("/slot-assignments/assign_and_generate/", {
      program_id: program.id,
      slot_template_id: Number(slotId),
      start_date: startDate
    });
    await load();
  }

  async function addNote() {
    if (!program?.id) return alert("No program");
    const session = program.sessions?.find(s => s.status === "SCHEDULED") || program.sessions?.[0];
    await api.post("/notes/", {
      program: program.id,
      session: session?.id || null,
      template: templateId,
      kind: "SESSION",
      data: { narrative: noteText }
    });
    setNoteText("");
    const n = await api.get("/notes/by_program", { params: { program_id: program.id } });
    setNotes(n.data);
  }

  return (
    <div>
      <h1 style={{ fontSize: 22 }}>Patient</h1>

      {patient && (
        <div className="card">
          <div style={{ fontSize: 18 }}><b>{patient.last_name}, {patient.first_name}</b></div>
          <div style={{ opacity: 0.85 }}>
            MRN: <span className="badge">{patient.mrn}</span>{" "}
            Gender: <span className="badge">{patient.gender}</span>{" "}
            Location: <span className="badge">{patient.location?.name || "-"}</span>
          </div>
        </div>
      )}

      <div style={{ height: 12 }} />
      <div className="grid2">
        <div className="card">
          <h2 style={{ fontSize: 16 }}>Program</h2>

          {!program && (
            <>
              <div style={{ opacity: 0.85 }}>No program yet.</div>
              <div style={{ height: 10 }} />
              <button className="btn primary" onClick={createProgram}>Create 22-session Program</button>
            </>
          )}

          {program && (
            <>
              <div style={{ opacity: 0.9, lineHeight: 1.8 }}>
                Status: <span className="badge">{program.status}</span><br />
                Sessions: <b>{program.sessions?.length || 0}</b> / <b>{program.total_sessions}</b><br />
                Start date: <b>{program.start_date || "-"}</b><br />
              </div>

              <div style={{ height: 10 }} />
              <label>Start date</label>
              <input className="input" type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />

              <div style={{ height: 8 }} />
              <label>Slot template (filtered by patient gender)</label>
              <select className="input" value={slotId} onChange={e => setSlotId(e.target.value)}>
                <option value="">Select slot...</option>
                {slots.map(s => (
                  <option key={s.id} value={s.id}>
                    {s.location?.name} | {s.therapist?.username} | {s.day1}/{s.day2} | {s.time_start} | allowed={s.patient_gender_allowed}
                  </option>
                ))}
              </select>

              <div style={{ height: 10 }} />
              <button className="btn primary" onClick={assignSlot}>Assign slot + generate 22 sessions</button>
            </>
          )}
        </div>

        <div className="card">
          <h2 style={{ fontSize: 16 }}>Therapist notes (internal)</h2>
          <label>Quick session note</label>
          <textarea className="input" rows={4} value={noteText} onChange={e => setNoteText(e.target.value)} placeholder="Session summary..." />
          <div style={{ height: 8 }} />
          <button className="btn primary" onClick={addNote}>Save note</button>

          <div style={{ height: 12 }} />
          <h3 style={{ fontSize: 14 }}>Recent notes</h3>
          <div style={{ display: "grid", gap: 8 }}>
            {notes.slice(0, 10).map(n => (
              <div key={n.id} className="card">
                <div style={{ opacity: 0.85, fontSize: 12 }}>
                  {new Date(n.created_at).toLocaleString()} • {n.therapist?.username || "—"}
                </div>
                <div style={{ marginTop: 6, whiteSpace: "pre-wrap" }}>
                  {n.data?.narrative || JSON.stringify(n.data)}
                </div>
              </div>
            ))}
            {!notes.length && <div style={{ opacity: 0.8 }}>No notes yet.</div>}
          </div>
        </div>
      </div>

      <div style={{ height: 12 }} />
      {program && (
        <div className="card">
          <h2 style={{ fontSize: 16 }}>Sessions</h2>
          <table>
            <thead><tr><th>#</th><th>Planned</th><th>Therapist</th><th>Status</th></tr></thead>
            <tbody>
              {program.sessions?.map(s => (
                <tr key={s.id}>
                  <td><span className="badge">{s.session_number}</span></td>
                  <td>{s.planned_start ? new Date(s.planned_start).toLocaleString() : "-"}</td>
                  <td>{s.therapist?.username || "-"}</td>
                  <td><span className="badge">{s.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
