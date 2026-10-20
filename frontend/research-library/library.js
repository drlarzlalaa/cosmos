import { apiRequest, getToken } from "/shared/api.js";

const resultsEl = document.getElementById("results");
const searchBox = document.getElementById("search-box");

function escapeHtml(s) {
  return String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function renderSources(sources) {
  if (!sources.length) {
    resultsEl.innerHTML = '<p class="muted">No sources yet.</p>';
    return;
  }
  resultsEl.innerHTML = sources.map((s) => `
    <div class="source">
      <span class="badge ${s.evidence_status}">${s.evidence_status.replace("_", " ")}</span>
      <h3>${escapeHtml(s.title)}</h3>
      <p>${escapeHtml(s.abstract)}</p>
      <p class="meta muted">
        ${s.authors ? escapeHtml(s.authors) + " &middot; " : ""}
        ${s.url ? `<a href="${escapeHtml(s.url)}" target="_blank" rel="noopener">source link</a> &middot; ` : ""}
        added ${escapeHtml(s.created_at)}
      </p>
    </div>
  `).join("");
}

async function runSearch() {
  const q = encodeURIComponent(searchBox.value.trim());
  const { sources } = await apiRequest("/api/sources?q=" + q);
  renderSources(sources);
}

let debounce = null;
searchBox.addEventListener("input", () => {
  clearTimeout(debounce);
  debounce = setTimeout(runSearch, 150);
});

runSearch();

if (getToken()) {
  document.getElementById("add-panel").style.display = "block";
  document.getElementById("add-submit").addEventListener("click", async () => {
    const errorEl = document.getElementById("add-error");
    errorEl.textContent = "";
    try {
      await apiRequest("/api/sources", {
        method: "POST",
        body: {
          title: document.getElementById("src-title").value,
          url: document.getElementById("src-url").value,
          authors: document.getElementById("src-authors").value,
          abstract: document.getElementById("src-abstract").value,
          evidence_status: document.getElementById("src-evidence").value,
        },
      });
      document.getElementById("src-title").value = "";
      document.getElementById("src-url").value = "";
      document.getElementById("src-authors").value = "";
      document.getElementById("src-abstract").value = "";
      runSearch();
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
} else {
  document.getElementById("signed-out-note").style.display = "block";
}
