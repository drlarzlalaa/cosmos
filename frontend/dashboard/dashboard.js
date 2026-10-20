import { apiRequest, clearToken, requireAuthOrRedirect } from "/shared/api.js";

if (requireAuthOrRedirect()) {
  apiRequest("/api/users/me")
    .then(({ user }) => {
      document.getElementById("whoami").textContent = user.display_name + " (" + user.email + ")";
    })
    .catch(() => {
      clearToken();
      window.location.href = "/login/";
    });
}

document.getElementById("logout").addEventListener("click", () => {
  clearToken();
  window.location.href = "/login/";
});

// Static for now - Phase 3/5/6/7 wire these to real engines/* modules
// as they land (see ROADMAP.md). Listed here so the dashboard honestly
// reflects what exists vs. what's planned.
const ENGINES = [
  { name: "Physics engine", phase: 3 },
  { name: "Mathematics engine", phase: 3 },
  { name: "Cosmic data engine", phase: 3 },
  { name: "Consciousness engine", phase: 6 },
  { name: "Causality engine", phase: 6 },
  { name: "Existence engine", phase: 6 },
  { name: "Spiritual research engine", phase: 6 },
  { name: "Universal discovery engine", phase: 7 },
];

const grid = document.getElementById("engine-grid");
for (const engine of ENGINES) {
  const card = document.createElement("div");
  card.className = "card";
  card.innerHTML = `<div>${engine.name}</div><span class="phase">Phase ${engine.phase} — not yet built</span>`;
  grid.appendChild(card);
}
