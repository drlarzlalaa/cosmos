import { apiRequest, getToken } from "/shared/api.js";

const ENGINE_NAME = "physics-engine/gravity";

const selectEl = document.getElementById("calc-select");
const formsEl = document.getElementById("calc-forms");
const errorEl = document.getElementById("calc-error");
const resultEl = document.getElementById("result");
const saveRowEl = document.getElementById("save-row");
const saveNoteEl = document.getElementById("save-note");
const findingsListEl = document.getElementById("findings-list");

let lastCalc = null;
let lastInputs = null;

function labelFor(param) {
  return param.replace(/_/g, " ");
}

function escapeHtml(s) {
  return String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function renderForms(calculations) {
  formsEl.innerHTML = "";
  for (const [name, spec] of Object.entries(calculations)) {
    const group = document.createElement("div");
    group.className = "calc-group";
    group.dataset.calc = name;
    group.innerHTML = `<p class="muted">${spec.formula} &rarr; ${spec.unit}</p>` +
      spec.params.map((p) => `<label>${labelFor(p)}</label><input data-param="${p}" type="number" step="any">`).join("");
    formsEl.appendChild(group);
  }
}

function showGroup(name) {
  document.querySelectorAll(".calc-group").forEach((g) => g.classList.toggle("active", g.dataset.calc === name));
}

async function loadFindings() {
  const { findings } = await apiRequest("/api/findings?engine=" + encodeURIComponent(ENGINE_NAME));
  if (!findings.length) {
    findingsListEl.innerHTML = '<p class="muted">No findings saved yet.</p>';
    return;
  }
  findingsListEl.innerHTML = findings.map((f) => `
    <div class="source">
      <span class="badge">${escapeHtml(f.evidence_status)}</span>
      <h3>${escapeHtml(f.calculation.replace(/_/g, " "))} = ${f.result} ${escapeHtml(f.unit)}</h3>
      <p class="meta muted">${escapeHtml(f.formula)} &middot; saved ${escapeHtml(f.created_at)}</p>
    </div>
  `).join("");
}

async function init() {
  const { calculations } = await apiRequest("/api/engines/gravity");
  selectEl.innerHTML = Object.keys(calculations).map((name) =>
    `<option value="${name}">${name.replace(/_/g, " ")}</option>`).join("");
  renderForms(calculations);
  showGroup(selectEl.value);
  selectEl.addEventListener("change", () => showGroup(selectEl.value));
  if (!getToken()) {
    document.getElementById("save-signed-out-note").style.display = "block";
  }
  await loadFindings();
}

document.getElementById("calc-submit").addEventListener("click", async () => {
  errorEl.textContent = "";
  resultEl.style.display = "none";
  saveRowEl.style.display = "none";
  const calc = selectEl.value;
  const inputs = {};
  document.querySelectorAll(`.calc-group[data-calc="${calc}"] input`).forEach((el) => {
    inputs[el.dataset.param] = parseFloat(el.value);
  });
  try {
    const data = await apiRequest("/api/engines/gravity", { method: "POST", body: { calculation: calc, inputs } });
    resultEl.textContent = `${data.result} ${data.unit}  (${data.formula})`;
    resultEl.style.display = "block";
    lastCalc = calc;
    lastInputs = inputs;
    if (getToken()) {
      saveNoteEl.textContent = "";
      saveRowEl.style.display = "block";
    }
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

document.getElementById("save-finding").addEventListener("click", async () => {
  try {
    await apiRequest("/api/findings", {
      method: "POST",
      body: { engine: ENGINE_NAME, calculation: lastCalc, inputs: lastInputs },
    });
    saveNoteEl.textContent = "Saved.";
    await loadFindings();
  } catch (err) {
    saveNoteEl.textContent = err.message;
  }
});

init();
