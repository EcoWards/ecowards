import { reciclar } from "./api.js";

const form = document.getElementById("reciclarForm");
const toast = document.getElementById("toastRecycle");

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

  }, 3000);
}

form.addEventListener("submit", async (e) => {

  e.preventDefault();

  const tipo = document.getElementById("tipo").value;

  const cantidad = parseInt(
    document.getElementById("cantidad").value
  );

  const res = await reciclar(tipo, cantidad);

  if (res.error) {
    showToast(res.error);
    return;
  }

  showToast(res.mensaje + " 🎉");

  setTimeout(() => {
    window.location.href = "index.html";
  }, 2000);
});

document.getElementById("volver")
.addEventListener("click", () => {
  window.location.href = "index.html";
});