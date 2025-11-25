# ASOPADEL

Sistema de Gestión para la Asociación de Pádel de Barinas

---

## 📋 Tabla de Contenidos

- [Instalación con Docker](#-instalación-con-docker-recomendado)
- [Instalación con Python Local](#-instalación-con-python-local)
- [Comandos Útiles](#-comandos-útiles)
- [Solución de Problemas](#️-solución-de-problemas)
- [Seguridad](#-seguridad)

---

## 🐳 Instalación con Docker (Recomendado)

### Requisitos

- Docker Desktop (Windows) o Docker Engine (Linux)
- Git

### Windows

1. **Instalar Docker Desktop**
    - Descargar de: <https://docs.docker.com/desktop/install/windows-install/>
    - Habilitar WSL 2 durante la instalación

2. **Clonar el proyecto**

    ```powershell
    git clone https://github.com/ErPyrex/asopadel.git
    cd asopadel
    ```

3. **Configurar variables de entorno**

    ```powershell
    copy .env.example .env
    ```

    Generar SECRET_KEY:

    ```powershell
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    Editar `.env` y pegar la SECRET_KEY generada.

4. **Ejecutar Docker**

    ```powershell
    docker compose up --build
    ```

5. **Crear superusuario** (en otra terminal PowerShell)

    ```powershell
    docker compose exec web python manage.py createsuperuser
    ```

6. **Acceder:** <http://localhost:8000>

### Linux

1. **Instalar Docker**

    ```bash
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install docker.io docker-compose-plugin
    
    # Post-instalación (ejecutar Docker sin sudo)
    sudo usermod -aG docker $USER
    newgrp docker
    ```

2. **Clonar el proyecto**

    ```bash
    git clone https://github.com/ErPyrex/asopadel.git
    cd asopadel
    ```

3. **Configurar variables de entorno**

    ```bash
    cp .env.example .env
    ```

    Generar SECRET_KEY:

    ```bash
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    Editar `.env` y pegar la SECRET_KEY generada.

4. **Ejecutar Docker**

    ```bash
    docker compose up --build
    ```

5. **Crear superusuario** (en otra terminal)

    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

6. **Acceder:** <http://localhost:8000>

---

## 💻 Instalación con Python Local

### Windows

#### Requisitos

- Python 3.10+ (desde python.org)
- PostgreSQL 16 (desde postgresql.org)
- Git

#### Pasos

1. **Clonar el proyecto**

    ```powershell
    git clone https://github.com/ErPyrex/asopadel.git
    cd asopadel
    ```

2. **Crear entorno virtual**

    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. **Instalar dependencias**

    ```powershell
    pip install -r requirements.txt
    ```

4. **Configurar .env**

    ```powershell
    copy .env.example .env
    ```

    Generar SECRET_KEY:

    ```powershell
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    Editar `.env`:
    - Pegar SECRET_KEY
    - Cambiar `@db:` por `@localhost:`

5. **Configurar PostgreSQL**

    Abrir SQL Shell (psql) desde el menú inicio:

    ```sql
    CREATE DATABASE asopadel_barinas;
    CREATE USER asopadel_user WITH PASSWORD 'postgres';
    GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
    ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
    ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';
    \c asopadel_barinas
    GRANT ALL ON SCHEMA public TO asopadel_user;
    \q
    ```

6. **Crear directorio de logs**

    ```powershell
    mkdir logs
    ```

7. **Aplicar migraciones**

    ```powershell
    python manage.py migrate
    ```

8. **Crear superusuario**

    ```powershell
    python manage.py createsuperuser
    ```

9. **Ejecutar servidor**

    ```powershell
    python manage.py runserver
    ```

10. **Acceder:** <http://localhost:8000>

### Linux

#### Requisitos

- Python 3.10+
- PostgreSQL 16
- Git

#### Pasos

1. **Instalar dependencias del sistema**

    ```bash
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install python3 python3-venv python3-pip postgresql postgresql-contrib git
    ```

2. **Clonar el proyecto**

    ```bash
    git clone https://github.com/ErPyrex/asopadel.git
    cd asopadel
    ```

3. **Crear entorno virtual**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Instalar dependencias**

    ```bash
    pip install -r requirements.txt
    ```

5. **Configurar .env**

    ```bash
    cp .env.example .env
    ```

    Generar SECRET_KEY:

    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    Editar `.env`:
    - Pegar SECRET_KEY
    - Cambiar `@db:` por `@localhost:`

6. **Configurar PostgreSQL**

    ```bash
    sudo -u postgres psql
    ```

    Dentro de psql:

    ```sql
    CREATE DATABASE asopadel_barinas;
    CREATE USER asopadel_user WITH PASSWORD 'postgres';
    GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
    ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
    ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';
    \c asopadel_barinas
    GRANT ALL ON SCHEMA public TO asopadel_user;
    \q
    ```

7. **Crear directorio de logs**

    ```bash
    mkdir -p logs
    ```

8. **Aplicar migraciones**

    ```bash
    python manage.py migrate
    ```

9. **Crear superusuario**

    ```bash
    python manage.py createsuperuser
    ```

10. **Ejecutar servidor**

    ```bash
    python manage.py runserver
    ```

11. **Acceder:** <http://localhost:8000>

---

## 🔧 Comandos Útiles

### Docker

```bash
# Ver logs en tiempo real
docker compose logs -f web

# Ver estado de contenedores
docker compose ps

# Detener contenedores
docker compose down

# Limpiar todo (⚠️ elimina datos)
docker compose down -v

# Ejecutar comandos Django
docker compose exec web python manage.py <comando>

# Acceder a PostgreSQL
docker compose exec db psql -U asopadel_user -d asopadel_barinas

# Ejecutar tests
docker compose exec web python manage.py test users --verbosity=2
```

### Python Local

**Windows (PowerShell):**

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test users --verbosity=2

# Recolectar estáticos
python manage.py collectstatic
```

**Linux:**

```bash
# Activar entorno virtual
source venv/bin/activate

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test users --verbosity=2

# Recolectar estáticos
python manage.py collectstatic
```

---

## ⚠️ Solución de Problemas

### Windows

**"docker-compose: command not found"**

- Usa `docker compose` (con espacio) en Docker Desktop

**"python: command not found"**

- Usa `py` en lugar de `python`
- O agrega Python al PATH del sistema

**"Permission denied" en PowerShell**

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**PostgreSQL no inicia**

- Verifica que el servicio esté corriendo en Servicios de Windows
- Inicia manualmente si es necesario

### Linux

**"docker: permission denied"**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

**"python: command not found"**

- Usa `python3` en lugar de `python`

**"Permission denied: logs/security.log"**

```bash
rm -f logs/security.log
touch logs/security.log
```

**PostgreSQL no inicia**

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Ambos Sistemas

**"password authentication failed"**

Verifica que `.env` tenga credenciales consistentes:

```env
DATABASE_URL=postgresql://asopadel_user:postgres@db:5432/asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=postgres
```

**Cambiar entre Docker y Local**

Para Docker:

```bash
# Windows
(Get-Content .env) -replace '@localhost:', '@db:' | Set-Content .env

# Linux
sed -i 's|@localhost:|@db:|g' .env
```

Para Local:

```bash
# Windows
(Get-Content .env) -replace '@db:', '@localhost:' | Set-Content .env

# Linux
sed -i 's|@db:|@localhost:|g' .env
```

---

## 🔒 Seguridad

### Características Implementadas

- ✅ Variables de entorno para secretos
- ✅ Rate limiting (5 intentos/minuto en login)
- ✅ Validación de archivos (5MB máx, solo imágenes)
- ✅ Separación de privilegios
- ✅ Headers de seguridad HTTP
- ✅ Sesiones seguras (timeout 1 hora)
- ✅ Logging de eventos de seguridad

### Importante

**Desarrollo:**

- `DEBUG=True`
- Contraseñas simples aceptables
- HTTP permitido

**Producción:**

- `DEBUG=False` (obligatorio)
- Contraseñas fuertes (12+ caracteres)
- HTTPS obligatorio
- Configurar todas las variables de seguridad

---

## 📚 Documentación Adicional

- **[DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md)** - Arquitectura, modelos, seguridad y detalles técnicos completos

---

## 🔄 Flujo de Trabajo Git

```bash
# 1. Crear rama desde main
git checkout main
git pull origin main
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios y commits
git add .
git commit -m "feat: descripción del cambio"

# 3. Ejecutar tests
python manage.py test

# 4. Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### Nomenclatura

**Ramas:**

- `feature/nombre-del-feature`
- `bugfix/nombre-del-bugfix`
- `security/nombre-del-fix`

**Commits:**

- `feat: nueva funcionalidad`
- `fix: corrección de bug`
- `security: corrección de vulnerabilidad`
- `docs: actualización de documentación`

---

## 👥 Contribución

1. No trabajar directamente en `main`
2. Seguir GitHubFlow
3. Ejecutar tests antes de PR
4. Usar nombres descriptivos en commits
5. Documentar cambios significativos

---

## 📄 Licencia

Proyecto privado - Asociación de Pádel de Barinas

---

## 🆘 Soporte

Para problemas o preguntas, consulta la [documentación técnica](DOCUMENTACION_TECNICA.md) o abre un issue en GitHub.
