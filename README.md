# ASOPADEL - Sistema de Gestión 🎾

Sistema integral para la gestión de la **Asociación de Pádel de Barinas**. Permite la administración de jugadores, árbitros, torneos, canchas y noticias de manera eficiente.

---

## 🚀 Inicio Rápido con Docker (Recomendado)

La forma más rápida de tener el proyecto corriendo es usando Docker.

1. **Clonar y configurar:**
   ```bash
   git clone https://github.com/ErPyrex/asopadel.git
   cd asopadel
   cp .env.example .env  # En Windows usa 'copy'
   ```

2. **Levantar el sistema:**
   ```bash
   docker compose up --build
   ```

3. **Crear tu primer usuario Administrador:**
   ```bash
   # En otra terminal
   docker compose exec web python manage.py createsuperuser
   ```

4. **Acceder:** [http://localhost:8000](http://localhost:8000)

---

## ✨ Características Principales

*   👤 **Roles Diferenciados:** Dashboards específicos para Jugadores, Árbitros y Administradores.
*   🏆 **Gestión de Torneos:** Registro de competiciones, partidos y resultados en tiempo real.
*   🎾 **Control de Instalaciones:** Gestión de canchas y disponibilidad.
*   📰 **Portal de Noticias:** Blog integrado para comunicados y novedades.
*   🛡️ **Seguridad Avanzada:** Login por cédula, protección contra fuerza bruta y sesiones seguras.
*   🌙 **Modo Oscuro/Claro:** Interfaz moderna y adaptable.

---

## 🛠️ Desarrollo y Despliegue

### Requisitos Locales (sin Docker)
*   Python 3.10+
*   PostgreSQL 16+
*   Pip / Venv

### Comandos Útiles
*   **Tests:** `docker compose exec web pytest`
*   **Migraciones:** `docker compose exec web python manage.py migrate`
*   **Logs:** `docker compose logs -f web`

### Despliegue en Render
El proyecto está optimizado para [Render](https://render.com/). Utiliza el archivo `render.yaml` para configurar automáticamente la base de datos y el servicio web.

---

## 📚 Documentación Detallada

Para información técnica profunda, consulta los siguientes archivos:

1.  **[DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md)**: Arquitectura, Modelos, Seguridad y Guías de desarrollo.
2.  **Guía de Despliegue**: Consultar sección de Render en el doc técnico.

---

## 👥 Contribución

1. Crea una rama (`feature/mejora`) desde `main`.
2. Sigue el flujo de trabajo de Git (Commits descriptivos: `feat:`, `fix:`, `docs:`).
3. Asegúrate de que los tests pasen antes de enviar un Pull Request.

---

## 📄 Licencia

Proyecto Privado - Asociación de Pádel de Barinas.
