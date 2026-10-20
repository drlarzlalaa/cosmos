import { apiRequest, setToken, getToken } from "/shared/api.js";

if (getToken()) window.location.href = "/dashboard/";

const loginView = document.getElementById("login-view");
const registerView = document.getElementById("register-view");

document.getElementById("show-register").addEventListener("click", (e) => {
  e.preventDefault();
  loginView.style.display = "none";
  registerView.style.display = "block";
});

document.getElementById("show-login").addEventListener("click", (e) => {
  e.preventDefault();
  registerView.style.display = "none";
  loginView.style.display = "block";
});

document.getElementById("login-submit").addEventListener("click", async () => {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;
  const errorEl = document.getElementById("login-error");
  errorEl.textContent = "";
  try {
    const data = await apiRequest("/api/auth/login", { method: "POST", body: { email, password } });
    setToken(data.token);
    window.location.href = "/dashboard/";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

document.getElementById("register-submit").addEventListener("click", async () => {
  const display_name = document.getElementById("register-name").value;
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;
  const errorEl = document.getElementById("register-error");
  errorEl.textContent = "";
  try {
    const data = await apiRequest("/api/auth/register", { method: "POST", body: { email, password, display_name } });
    setToken(data.token);
    window.location.href = "/dashboard/";
  } catch (err) {
    errorEl.textContent = err.message;
  }
});
