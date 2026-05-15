const BASE_URL = "https://TU-PROYECTO.up.railway.app/api";

/* =========================
   🔐 LOGIN
========================= */
export async function login(username, password) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (data.error) return data;

  // guardar sesión
  localStorage.setItem("session", data.username);

  return data;
}

/* =========================
   👤 USUARIO
========================= */
export async function getUser() {
  const username = localStorage.getItem("session");

  const res = await fetch(`${BASE_URL}/user/${username}`);
  return await res.json();
}

/* =========================
   📜 HISTORIAL
========================= */
export async function getHistorial() {
  const username = localStorage.getItem("session");

  const res = await fetch(`${BASE_URL}/historial/${username}`);
  return await res.json();
}

/* =========================
   🎁 RECOMPENSAS
========================= */
export async function getRewards() {
  const res = await fetch(`${BASE_URL}/rewards`);
  return await res.json();
}

/* =========================
   🏆 RANKING
========================= */
export async function getRanking() {
  const res = await fetch(`${BASE_URL}/ranking`);
  return await res.json();
}

/* =========================
   ♻️ RECICLAR
========================= */
export async function reciclar(tipo, cantidad) {
  const username = localStorage.getItem("session");

  const res = await fetch(`${BASE_URL}/reciclar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      tipo,
      cantidad
    })
  });

  return await res.json();
}

/* =========================
   🎁 CANJEAR
========================= */
export async function canjear(rewardId) {
  const username = localStorage.getItem("session");

  const res = await fetch(`${BASE_URL}/canjear`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      rewardId
    })
  });

  return await res.json();
}

/* =========================
   ♻️ MATERIALES
========================= */
export async function getMateriales() {
  // opcional: lo puedes mover al backend después
  return [
    { nombre: "Botella", valor: 3 },
    { nombre: "Lata", valor: 4 },
    { nombre: "Papel", valor: 1 },
    { nombre: "Cartón", valor: 2 }
  ];
}