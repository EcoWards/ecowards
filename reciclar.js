import { reciclar } from "./api.js";

/* 🔐 PROTEGER RUTA */
if (!localStorage.getItem("session")) {
  window.location.href = "login.html";
}

const form =
  document.getElementById("reciclarForm");

const toast =
  document.getElementById("toastRecycle");

const volverBtn =
  document.getElementById("volver");

/* 💬 TOAST */
function showToast(msg) {

  toast.textContent = msg;

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

/* ♻️ RECICLAR */
form.addEventListener("submit", async (e) => {

  e.preventDefault();

  const tipo =
    document.getElementById("tipo").value;

  const cantidad = parseInt(
    document.getElementById("cantidad").value
  );

  if (!cantidad || cantidad <= 0) {

    showToast("Cantidad inválida");

    return;
  }

  try {

    const res = await reciclar(
      tipo,
      cantidad
    );

    if (res.error) {

      showToast(res.error);
      return;
    }

    showToast(res.mensaje + " 🎉");

    setTimeout(() => {
      window.location.href = "index.html";
    }, 1500);

  } catch (err) {

    showToast("Error al reciclar");
    console.error(err);
  }
});

/* 🔙 VOLVER */
if (volverBtn) {

  volverBtn.addEventListener("click", () => {

    window.location.href = "index.html";
  });
}