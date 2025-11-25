# Guía Rápida de Instalación - ASOPADEL

## 🚀 Opción 1: Docker (Recomendado)

### Requisitos

- Docker Desktop (Windows) o Docker Engine (Linux)
- Git

### Pasos

1. **Clonar repositorio:**

   ```bash
   git clone https://github.com/ErPyrex/asopadel.git
   cd asopadel
   ```

2. **Crear archivo .env:**

   ```bash
   cp .env.example .env
   ```

3. **Generar SECRET_KEY:**

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Editar .env:**
   - Pegar la SECRET_KEY generada
   - Cambiar `password_seguro` por una contraseña fuerte

5. **Ejecutar Docker:**

   ```bash
   docker-compose up --build
   ```

6. **Crear superusuario (en otra terminal):**

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

7. **Acceder:**
   - <http://localhost:8000>

---

## 💻 Opción 2: Instalación Local

### Requisitos

- Python 3.10+
- PostgreSQL 16
- Git

### Pasos

1. **Clonar repositorio:**

   ```bash
   git clone https://github.com/ErPyrex/asopadel.git
   cd asopadel
   ```

2. **Crear entorno virtual:**

   **Windows:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

   **Linux/macOS:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear archivo .env:**

   ```bash
   cp .env.example .env
   ```

5. **Generar SECRET_KEY:**

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Editar .env:**
   - Pegar la SECRET_KEY generada
   - Configurar DATABASE_URL con tus credenciales de PostgreSQL

7. **Configurar PostgreSQL:**

   **Windows (PowerShell):**

   ```powershell
   psql -U postgres
   ```

   **Linux/macOS:**

   ```bash
   sudo -u postgres psql
   ```

   **Dentro de psql:**

   ```sql
   CREATE DATABASE asopadel_barinas;
   CREATE USER asopadel_user WITH PASSWORD 'tu_password_seguro';
   ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
   ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';
   GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
   \q
   ```

8. **Crear directorio de logs:**

   ```bash
   mkdir -p logs
   ```

9. **Aplicar migraciones:**

   ```bash
   python manage.py migrate
   ```

10. **Crear superusuario:**

    ```bash
    python manage.py createsuperuser
    ```

11. **Ejecutar servidor:**

    ```bash
    python manage.py runserver
    ```

12. **Acceder:**
    - <http://localhost:8000>

---

## ⚠️ Problemas Comunes

### "python: command not found"

- **Linux/macOS:** Usa `python3` en lugar de `python`
- **Windows:** Usa `py` en lugar de `python`

### "ModuleNotFoundError: No module named 'django'"

- Asegúrate de haber activado el entorno virtual
- Ejecuta `pip install -r requirements.txt`

### "SECRET_KEY not found"

- Verifica que el archivo `.env` existe
- Verifica que `SECRET_KEY` está definido en `.env`

### Error de conexión a PostgreSQL

- Verifica que PostgreSQL está corriendo
- Verifica las credenciales en `.env`
- En Docker, verifica que el contenedor `db` está activo

### "Rate limited" en login

- Has excedido 5 intentos de login por minuto
- Espera 1 minuto antes de intentar nuevamente

---

## 📚 Documentación Completa

- [README.md](file:///home/pyrex64/Escritorio/asopadel/README.md) - Guía completa
- [DOCUMENTACION_TECNICA.md](file:///home/pyrex64/Escritorio/asopadel/DOCUMENTACION_TECNICA.md) - Documentación técnica
