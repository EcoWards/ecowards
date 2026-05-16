const BASE_URL =
  "https://ecowards-production.up.railway.app/api";

/* 🔐 SI YA HAY SESIÓN */
if (localStorage.getItem("session")) {
  window.location.href = "index.html";
}

document.getElementById("registerForm")
.addEventListener("submit", async (e) => {

  e.preventDefault();

  const nombre =
    document.getElementById("nombre").value;

  const username =
    document.getElementById("username").value;

  const password =
    document.getElementById("password").value;

  const errorMsg =
    document.getElementById("errorMsg");

  const res = await fetch(`${BASE_URL}/register`, {

    method: "POST",

    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify({
      nombre,
      username,
      password
    })
  });

  const data = await res.json();

  if (data.error) {

    errorMsg.textContent = data.error;

  } else {

    localStorage.setItem(
      "session",
      username
    );

    window.location.href = "index.html";
  }

});