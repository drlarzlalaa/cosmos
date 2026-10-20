// Tiny fetch wrapper shared by every COSMOS frontend page. No build
// step, no framework - plain ES modules served straight by the
// stdlib static file handler in backend/api-gateway/server.py.
const TOKEN_KEY = "cosmos_token";

export function getToken() {
  try { return localStorage.getItem(TOKEN_KEY); } catch (e) { return null; }
}

export function setToken(token) {
  try { localStorage.setItem(TOKEN_KEY, token); } catch (e) { /* ignore */ }
}

export function clearToken() {
  try { localStorage.removeItem(TOKEN_KEY); } catch (e) { /* ignore */ }
}

export async function apiRequest(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers["Authorization"] = "Bearer " + token;
  const res = await fetch(path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || ("request failed: " + res.status));
  return data;
}

export function requireAuthOrRedirect() {
  if (!getToken()) {
    window.location.href = "/login/";
    return false;
  }
  return true;
}
