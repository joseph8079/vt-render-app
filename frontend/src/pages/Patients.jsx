import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { PatientFormModal } from "../components/PatientFormModal";

type Patient = {
  id: number;
  first_name: string;
  last_name: string;
  dob?: string | null;
  location?: number | null;
};

export default function Patients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAddOpen, setIsAddOpen] = useState(false);

  async function load() {
    setLoading(true);
    try {
      const res = await api.get("/patients/");
      // DRF might return list or paginated {results:[]}
      const data = res.data?.results ?? res.data ?? [];
      setPatients(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function createPatient(payload: any) {
    const res = await api.post("/patients/", payload);
    const created = res.data;
    setPatients((prev) => [created, ...prev]);
  }

  return (
    <div style={{ padding: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Patients</h2>
        <button onClick={() => setIsAddOpen(true)}>+ Add Patient</button>
      </div>

      {loading ? (
        <p>Loading…</p>
      ) : patients.length === 0 ? (
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>
          <p>No patients yet.</p>
          <button onClick={() => setIsAddOpen(true)}>Add your first patient</button>
        </div>
      ) : (
        <table width="100%" cellPadding={8} style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ textAlign: "left", borderBottom: "1px solid #ddd" }}>
              <th>Name</th>
              <th>DOB</th>
              <th>ID</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                <td>{p.first_name} {p.last_name}</td>
                <td>{p.dob ?? "-"}</td>
                <td>{p.id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <PatientFormModal
        open={isAddOpen}
        title="Add Patient"
        onClose={() => setIsAddOpen(false)}
        onSubmit={async (payload) => {
          await createPatient(payload);
          setIsAddOpen(false);
        }}
      />
    </div>
  );
}
