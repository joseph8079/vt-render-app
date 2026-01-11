import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { clearTokens } from "./auth";
import { setAuthToken } from "./api";

export default function Layout({ children }) {
  const nav = useNavigate();
  return (
    <>
      <div className="nav">
        <strong style={{ marginRight: 6 }}>VT Ops</strong>
        <NavLink to="/dashboard" className={({ isActive }) => (isActive ? "active" : "")}>Dashboard</NavLink>
        <NavLink to="/pipeline" className={({ isActive }) => (isActive ? "active" : "")}>Pipeline</NavLink>
        <NavLink to="/patients" className={({ isActive }) => (isActive ? "active" : "")}>Patients</NavLink>
        <NavLink to="/slots" className={({ isActive }) => (isActive ? "active" : "")}>Slots</NavLink>
        <div style={{ flex: 1 }} />
        <button className="btn" onClick={() => { clearTokens(); setAuthToken(null); nav("/login"); }}>Logout</button>
      </div>
      <div className="container">{children}</div>
    </>
  );
}
