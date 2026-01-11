import { useEffect, useState } from "react";
import { api } from "../api/client";

export function PatientFormModal({
  open,
  title,
  onClose,
  onSubmit,
}: {
  open: boolean;
  title: string;
  onClose: () => void;
  onSubmit: (payload: any) => Promise<void>;
}) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [dob, setDob] = useState("");
  const [locationId, setLocationId] = useState<string>("");
  const [locations, setLocations] = useState<{ id: number; name: string }[]>([]);
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setErr(null);
    (async () => {
      try {
        // If your API exposes /locations/
        const res = await api.get("/locations/");
        const data = res.data?.results ?? res.data ?? [];
        setLocations(data);
      } catch {
        // If endpoint doesn't exist, just allow manual numeric id.
        setLocations([]);
      }
    })();
  }, [open]);

  if (!open) return null;

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.35)",
      display: "flex", alignItems: "center", justifyContent: "center"
    }}>
      <div style={{ width: 520, background: "#fff", borderRadius: 10, padding: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h3 style={{ margin: 0 }}>{title}</h3>
          <button onClick={onClose}>✕</button>
        </div>

        <div style={{ marginTop: 12, display: "grid", gap: 10 }}>
          <label>
            First name
            <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
          </label>
          <label>
            Last name
            <input value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </label>
          <label>
            DOB
            <input type="date" value={dob} onChange={(e) => setDob(e.target.value)} />
          </label>

          <label>
            Location
            {locations.length ? (
              <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
                <option value="">Select…</option>
                {locations.map((l) => (
                  <option key={l.id} value={String(l.id)}>{l.name}</option>
                ))}
              </select>
            ) : (
              <input
                placeholder="Location ID (optional)"
                value={locationId}
                onChange={(e) => setLocationId(e.target.value)}
              />
            )}
          </label>

          {err && <div style={{ color: "crimson" }}>{err}</div>}

          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
            <button onClick={onClose} disabled={saving}>Cancel</button>
            <button
              onClick={async () => {
                setSaving(true);
                setErr(null);
                try {
                  await onSubmit({
                    first_name: firstName.trim(),
                    last_name: lastName.trim(),
                    dob: dob || null,
                    location: locationId ? Number(locationId) : null,
                  });
                } catch (e: any) {
                  const msg = e?.response?.data ? JSON.stringify(e.response.data) : "Failed to create patient";
                  setErr(msg);
                } finally {
                  setSaving(false);
                }
              }}
              disabled={saving || !firstName.trim() || !lastName.trim()}
            >
              {saving ? "Saving…" : "Create"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
