import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, setAuthToken } from "../app/api";
import { saveTokens } from "../app/auth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const nav = useNavigate();

  return (
    <div className="container" style={{ maxWidth: 520, marginTop: 70 }}>
      <div className="card">
        <h1 style={{ fontSize: 22 }}>Sign in</h1>

        <label>Username</label>
        <input className="input" value={username} onChange={(e) => setUsername(e.target.value)} />

        <div style={{ height: 10 }} />

        <label>Password</label>
        <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

        <div style={{ height: 12 }} />
        {err && <div className="card" style={{ borderColor: "rgba(255,0,90,0.5)" }}>{err}</div>}
        <div style={{ height: 12 }} />

        <button className="btn primary" onClick={async () => {
          setErr("");
          try {
            const tokens = await login(username, password);
            saveTokens(tokens);
            setAuthToken(tokens.access);
            nav("/dashboard");
          } catch (e) {
            setErr(e?.response?.data?.detail || "Login failed");
          }
        }}>Login</button>

        <p style={{ opacity: 0.8, marginTop: 12, fontSize: 13 }}>
          After running <code>python manage.py seed_demo</code>:
          <br /><code>vt_manager</code>, <code>intake</code>, <code>reviewer</code>, <code>therapist_m1</code>, <code>therapist_f1</code>
          <br />Password: <code>password</code>
        </p>
      </div>
    </div>
  );
}
