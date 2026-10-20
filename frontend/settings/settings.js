import { apiRequest, clearToken, requireAuthOrRedirect } from "/shared/api.js";

if (requireAuthOrRedirect()) {
  apiRequest("/api/users/me")
    .then(({ user }) => {
      document.getElementById("display-name").textContent = user.display_name;
      document.getElementById("email").textContent = user.email;
      document.getElementById("created-at").textContent = user.created_at;
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
