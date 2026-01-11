export function loadTokens() {
  try { return JSON.parse(localStorage.getItem("vt_tokens") || "null"); }
  catch { return null; }
}
export function saveTokens(tokens) {
  localStorage.setItem("vt_tokens", JSON.stringify(tokens));
}
export function clearTokens() {
  localStorage.removeItem("vt_tokens");
}
