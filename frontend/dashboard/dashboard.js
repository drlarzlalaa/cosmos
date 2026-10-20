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
// reflects what exists vs. what's planned. Physics is the one
// exception: gravity.py is real, built early out of roadmap order to
// prove the engine pipeline - see ROADMAP.md's "early Phase 3 slice".
const ENGINES = [
  { name: "Physics engine", phase: 3, status: "gravity calculations live", href: "/physics-explorer/" },
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
  const label = engine.status || "not yet built";
  const body = engine.href
    ? `<a href="${engine.href}">${engine.name}</a>`
    : `<div>${engine.name}</div>`;
  card.innerHTML = `${body}<span class="phase">Phase ${engine.phase} — ${label}</span>`;
  grid.appendChild(card);
}
