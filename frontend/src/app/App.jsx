import React, { useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Layout from "./Layout.jsx";
import Login from "../pages/Login.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import Pipeline from "../pages/Pipeline.jsx";
import Patients from "../pages/Patients.jsx";
import PatientDetail from "../pages/PatientDetail.jsx";
import Slots from "../pages/Slots.jsx";
import { loadTokens } from "./auth";
import { setAuthToken } from "./api";

function Private({ children }) {
  const tokens = loadTokens();
  const loc = useLocation();
  if (!tokens?.access) return <Navigate to="/login" replace state={{ from: loc.pathname }} />;
  return children;
}

export default function App() {
  useEffect(() => {
    const tokens = loadTokens();
    if (tokens?.access) setAuthToken(tokens.access);
  }, []);

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<Private><Layout><Dashboard /></Layout></Private>} />
      <Route path="/pipeline" element={<Private><Layout><Pipeline /></Layout></Private>} />
      <Route path="/patients" element={<Private><Layout><Patients /></Layout></Private>} />
      <Route path="/patients/:id" element={<Private><Layout><PatientDetail /></Layout></Private>} />
      <Route path="/slots" element={<Private><Layout><Slots /></Layout></Private>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
