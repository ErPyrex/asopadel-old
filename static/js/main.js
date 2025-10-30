// Animación de entrada para el hero
document.addEventListener("DOMContentLoaded", () => {
  const hero = document.querySelector(".hero-home");
  if (hero) {
    hero.style.opacity = 0;
    setTimeout(() => {
      hero.style.opacity = 1;
    }, 300);
  }
});

// Scroll suave a secciones con data-target
document.querySelectorAll(".btn-scroll").forEach(btn => {
  btn.addEventListener("click", e => {
    e.preventDefault();
    const targetSelector = btn.dataset.target;
    const target = document.querySelector(targetSelector);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});


document.addEventListener('DOMContentLoaded', () => {
    
    // --- Contador Animado para Métricas (Dashboard Admin) ---
    const metricCounters = document.querySelectorAll('.metric-value');

    const animateCounter = (el) => {
        const target = parseInt(el.getAttribute('data-target'));
        let current = 0;
        const duration = 1000; // 1 segundo
        const step = Math.ceil(target / (duration / 10));

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                clearInterval(timer);
                el.textContent = target.toLocaleString(); // Asegura el valor final y formato
            } else {
                el.textContent = current.toLocaleString();
            }
        }, 10);
    };

    // Usar Intersection Observer para que la animación inicie al ser visible
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5 // Inicia cuando el 50% del elemento es visible
    };

    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // El elemento está visible, iniciar animación
                animateCounter(entry.target);
                // Dejar de observar para que no se repita
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    metricCounters.forEach(counter => {
        counterObserver.observe(counter);
    });

    // --- Efecto Hover con JavaScript (Opcional, CSS ya hace mucho) ---
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-3px)';
            card.style.boxShadow = 'var(--shadow-hover)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'var(--shadow-base)';
        });
    });

});