document.addEventListener("DOMContentLoaded", () => {
  const carrusel = document.querySelector(".grid-noticias");
  if (!carrusel) return;

  // Duplicar contenido para efecto infinito
  carrusel.innerHTML += carrusel.innerHTML;

  // Estilo necesario
  carrusel.style.display = "flex";
  carrusel.style.whiteSpace = "nowrap";
  carrusel.parentElement.style.overflow = "hidden";

  let scrollAmount = 0;
  const velocidad = 3; // Ajusta la velocidad aquí

  function autoScroll() {
    carrusel.scrollLeft += velocidad;

    // Reinicia cuando llega a la mitad del contenido duplicado
    if (carrusel.scrollLeft >= carrusel.scrollWidth / 2) {
      carrusel.scrollLeft = 0;
    }

    requestAnimationFrame(autoScroll);
  }

  autoScroll();
});