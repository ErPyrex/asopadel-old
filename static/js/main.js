// Animación de entrada para el hero
document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".hero-home");
    if (hero) {
        hero.style.opacity = 0;
        setTimeout(() => {
            hero.style.opacity = 1;
        }, 300);
    }

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



});

// =======================================================
// === LÓGICA MODO OSCURO (BOOTSTRAP THEME TOGGLER ADAPTADO)
// === Implementación del selector de tema avanzado de Bootstrap
// =======================================================

(() => {
    "use strict";

    const storedTheme = localStorage.getItem("theme");

    const getPreferredTheme = () => {
        if (storedTheme) {
            return storedTheme;
        }

        return window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light";
    };

    const setTheme = function (theme) {
        let themeToApply = theme;

        // Determinar el tema final a aplicar, manejando el caso 'auto'
        if (
            theme === "auto" &&
            window.matchMedia("(prefers-color-scheme: dark)").matches
        ) {
            themeToApply = "dark";
        } else if (theme === "auto") {
            themeToApply = "light";
        }

        // 1. Aplicar el atributo de Bootstrap al HTML (Controla estilos de componentes de Bootstrap)
        document.documentElement.setAttribute("data-bs-theme", themeToApply);

        // 2. ADAPTACIÓN CRÍTICA PARA TU CSS:
        // Añadir/Quitar la clase 'dark-mode' del root (Necesario para tu fondo y estilos personalizados)
        if (themeToApply === "dark") {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }
    };

    setTheme(getPreferredTheme());

    const showActiveTheme = (theme) => {
        const activeThemeIcon = document.querySelector(".theme-icon-active use");
        // Usamos document.documentElement para buscar el tema si está en 'auto' y no en 'light' o 'dark'
        const currentTheme = document.documentElement.getAttribute('data-bs-theme') || theme;

        // Determinar el icono a mostrar en el botón principal
        let svgIconHref;
        if (currentTheme === 'light') {
            svgIconHref = '#sun-fill';
        } else if (currentTheme === 'dark') {
            svgIconHref = '#moon-stars-fill';
        } else {
            svgIconHref = '#circle-half';
        }

        if (activeThemeIcon) {
            activeThemeIcon.setAttribute("href", svgIconHref);
        }

        // Marcar el botón correcto como 'active' en el menú desplegable
        document.querySelectorAll("[data-bs-theme-value]").forEach((element) => {
            element.classList.remove("active");
        });

        const btnToActive = document.querySelector(
            `[data-bs-theme-value="${theme}"]`
        );
        if (btnToActive) {
            btnToActive.classList.add("active");
        }
    };

    window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", () => {
            if (storedTheme !== "light" || storedTheme !== "dark") {
                setTheme(getPreferredTheme());
            }
        });

    window.addEventListener("DOMContentLoaded", () => {
        showActiveTheme(getPreferredTheme());

        document.querySelectorAll("[data-bs-theme-value]").forEach((toggle) => {
            toggle.addEventListener("click", () => {
                const theme = toggle.getAttribute("data-bs-theme-value");
                localStorage.setItem("theme", theme);
                setTheme(theme);
                showActiveTheme(theme);
            });
        });
    });
})();