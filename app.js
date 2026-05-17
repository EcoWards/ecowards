import {
  getUser,
  getHistorial,
  getRewards,
  getRanking,
  getMateriales,
  canjear
} from "./api.js";

/* 🔐 PROTEGER RUTA */
if (!localStorage.getItem("session")) {
  window.location.href = "login.html";
}

/* 🚪 LOGOUT */
document.getElementById("logoutBtn")
.addEventListener("click", () => {

  localStorage.removeItem("session");
  localStorage.removeItem("user");

  window.location.href = "login.html";
});

/* 📦 MODAL */
const modal =
  document.getElementById("modal");

const modalText =
  document.getElementById("modalText");

const confirmBtn =
  document.getElementById("confirmBtn");

const cancelBtn =
  document.getElementById("cancelBtn");

const confirmView =
  document.getElementById("confirmView");

const couponView =
  document.getElementById("couponView");

const couponCode =
  document.getElementById("couponCode");

const couponReward =
  document.getElementById("couponReward");

const closeCoupon =
  document.getElementById("closeCoupon");

let rewardSeleccionado = null;

/* 🎲 GENERAR CÓDIGO */
function generarCodigo() {

  return Math.random()
    .toString(36)
    .substring(2, 10)
    .toUpperCase();
}

/* 🔄 CARGAR DASHBOARD */
async function loadDashboard() {

  const user = await getUser();

  document.getElementById("username")
    .textContent = user.nombre;

  document.getElementById("coins")
    .textContent = user.ecoCoins;

  document.getElementById("items")
    .textContent = user.objetos;

  /* HISTORIAL */
  const historyList =
    document.getElementById("history");

  const historial =
    await getHistorial();

  historyList.innerHTML = "";

  historial.forEach(item => {

    const li =
      document.createElement("li");

    li.textContent = item;

    historyList.appendChild(li);
  });

  /* REWARDS */
  const rewardsContainer =
    document.getElementById("rewards");

  const rewards =
    await getRewards();

  rewardsContainer.innerHTML = "";

  rewards.forEach(r => {

    const div =
      document.createElement("div");

    div.className = "reward";

    const btn =
      document.createElement("button");

    if (user.ecoCoins < r.costo) {

      btn.disabled = true;

      btn.classList.add(
        "btn-disabled"
      );

      btn.textContent =
        "No alcanza";

    } else {

      btn.textContent =
        "Canjear";

      btn.addEventListener(
        "click",
        () => {

          rewardSeleccionado = r;

          modalText.textContent =
            `¿Seguro que quieres canjear ${r.nombre} por ${r.costo} EcoCoins?`;

          modal.classList.remove(
            "hidden"
          );
        }
      );
    }

    div.innerHTML = `
      <strong>${r.nombre}</strong>
      <p>${r.costo} EC</p>
    `;

    div.appendChild(btn);

    rewardsContainer.appendChild(div);
  });

  /* RANKING */
  const rankingList =
    document.getElementById("ranking");

  const ranking =
    await getRanking();

  rankingList.innerHTML = "";

  ranking.forEach(r => {

    const li =
      document.createElement("li");

    li.textContent =
      `${r.nombre} - ${r.puntos}`;

    rankingList.appendChild(li);
  });

  /* MATERIALES */
  const materialsContainer =
    document.getElementById("materials");

  const materiales =
    await getMateriales();

  materialsContainer.innerHTML = "";

  materiales.forEach(m => {

    const div =
      document.createElement("div");

    div.className =
      "material-item";

    div.innerHTML = `
      <span>${m.nombre}</span>
      <span>+${m.valor} EC</span>
    `;

    materialsContainer.appendChild(div);
  });
}

/* 💬 TOAST */
function showToast(message) {

  const toast =
    document.getElementById("toast");

  if (!toast) return;

  toast.textContent = message;

  toast.classList.remove("hidden");

  setTimeout(() => {
    toast.classList.add("show");
  }, 10);

  setTimeout(() => {

    toast.classList.remove("show");

    setTimeout(() => {
      toast.classList.add("hidden");
    }, 300);

  }, 2500);
}

/* ✅ CONFIRMAR CANJE */
confirmBtn.addEventListener(
  "click",
  async () => {

    if (!rewardSeleccionado)
      return;

    const res =
      await canjear(
        rewardSeleccionado.id
      );

    if (res.error) {

      showToast(res.error);

      modal.classList.add(
        "hidden"
      );

      return;
    }

    confirmView.classList.add(
      "hidden"
    );

    couponView.classList.remove(
      "hidden"
    );

    couponReward.textContent =
      rewardSeleccionado.nombre;

    couponCode.textContent =
      generarCodigo();

    loadDashboard();
  }
);

/* ❌ CANCELAR */
cancelBtn.addEventListener(
  "click",
  () => {

    modal.classList.add(
      "hidden"
    );
  }
);

/* 🔒 CERRAR CUPÓN */
if (closeCoupon) {

  closeCoupon.addEventListener(
    "click",
    () => {

      modal.classList.add(
        "hidden"
      );

      couponView.classList.add(
        "hidden"
      );

      confirmView.classList.remove(
        "hidden"
      );
    }
  );
}

/* ♻️ BOTÓN RECICLAR */
document.getElementById("recycleBtn")
.addEventListener("click", () => {

  window.location.href =
    "reciclar.html";
});

/* 🚀 INICIAR */
loadDashboard();

/* =========================
   📢 ADS ROTATIVOS
========================= */

const adImage =
  document.getElementById("adImage");

const anuncios = [
  "img/ad1.png",
  "img/ad2.png",
  "img/ad3.png"
];

let currentAd = 0;

if (adImage) {

  setInterval(() => {

    currentAd++;

    if (
      currentAd >= anuncios.length
    ) {
      currentAd = 0;
    }

    adImage.src =
      anuncios[currentAd];

  }, 4000);
}