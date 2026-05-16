import { login } from "./api.js";

/* 🔐 SI YA HAY SESIÓN */
if (localStorage.getItem("session")) {
  window.location.href = "index.html";
}

document.getElementById("loginForm")
.addEventListener("submit", async (e) => {

  e.preventDefault();

  const username =
    document.getElementById("username").value;

  const password =
    document.getElementById("password").value;

  const errorMsg =
    document.getElementById("errorMsg");

  const res = await login(username, password);

  if (res.error) {

    errorMsg.textContent = res.error;

  } else {

    window.location.href = "index.html";
  }

});