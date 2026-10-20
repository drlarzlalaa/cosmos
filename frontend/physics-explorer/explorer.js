import { apiRequest } from "/shared/api.js";

const selectEl = document.getElementById("calc-select");
const formsEl = document.getElementById("calc-forms");
const errorEl = document.getElementById("calc-error");
const resultEl = document.getElementById("result");

function labelFor(param) {
  return param.replace(/_/g, " ");
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

async function init() {
  const { calculations } = await apiRequest("/api/engines/gravity");
  selectEl.innerHTML = Object.keys(calculations).map((name) =>
    `<option value="${name}">${name.replace(/_/g, " ")}</option>`).join("");
  renderForms(calculations);
  showGroup(selectEl.value);
  selectEl.addEventListener("change", () => showGroup(selectEl.value));
}

document.getElementById("calc-submit").addEventListener("click", async () => {
  errorEl.textContent = "";
  resultEl.style.display = "none";
  const calc = selectEl.value;
  const inputs = {};
  document.querySelectorAll(`.calc-group[data-calc="${calc}"] input`).forEach((el) => {
    inputs[el.dataset.param] = parseFloat(el.value);
  });
  try {
    const data = await apiRequest("/api/engines/gravity", { method: "POST", body: { calculation: calc, inputs } });
    resultEl.textContent = `${data.result} ${data.unit}  (${data.formula})`;
    resultEl.style.display = "block";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

init();
