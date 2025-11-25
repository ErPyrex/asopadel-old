# ASOPADEL

Sistema de Gestión para la Asociación de Pádel de Barinas

## 📋 Tabla de Contenidos

- [Requerimientos](#requerimientos)
- [Instalación para Desarrollo](#instalación-para-desarrollo)
- [Instalación con Docker (Recomendado)](#instalación-con-docker-recomendado)
- [Configuración de Seguridad](#configuración-de-seguridad)
- [Modo Desarrollo vs Producción](#modo-desarrollo-vs-producción)
- [Tests](#tests)
- [Flujo de Trabajo Git](#flujo-de-trabajo-git)

---

## 🔧 Requerimientos

### Instalación Manual

- **Python** 3.10 o superior

- **Git**
- **PostgreSQL** 16
- **pip** y **virtualenv**

### Instalación con Docker (Recomendado)

- **Docker Engine**

- **Docker Compose**

---

## 💻 Instalación para Desarrollo

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ErPyrex/asopadel.git
cd asopadel
```

### 2. Crear Entorno Virtual

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

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

**IMPORTANTE:** El proyecto requiere un archivo `.env` para funcionar.

1. Copia el archivo de ejemplo:

   ```bash
   cp .env.example .env
   ```

2. Genera una clave secreta segura:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Edita el archivo `.env` y configura las variables:

```env
# Django Configuration
SECRET_KEY=tu-clave-secreta-generada-aqui
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql://asopadel_user:tu_password_seguro@localhost:5432/asopadel_barinas

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Configuration
POSTGRES_DB=asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=tu_password_seguro

# Security Settings (Development)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

> ⚠️ **NUNCA** subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.

### 5. Configurar PostgreSQL

**Windows:**

```powershell
# Abrir SQL Shell (psql)
psql -U postgres

# Dentro de psql:
CREATE DATABASE asopadel_barinas;
CREATE USER asopadel_user WITH PASSWORD 'tu_password_seguro';
ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';
GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
\q
```

**Linux/macOS:**

```bash
sudo -u postgres psql
# Luego ejecutar los mismos comandos SQL de arriba
```

### 6. Crear Directorio de Logs

```bash
mkdir -p logs
```

### 7. Aplicar Migraciones

**Linux/macOS:**

```bash
python manage.py migrate
```

**Windows:**

```powershell
python manage.py migrate
```

> 💡 Si `python` no funciona, intenta con `python3` en Linux/macOS o `py` en Windows.

### 8. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa:

- **Cédula:** Tu número de identificación (será tu usuario)
- **Email:** Tu correo electrónico
- **Nombre y Apellido**
- **Contraseña:** Mínimo 10 caracteres

### 9. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

Accede a: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Instalación con Docker (Recomendado)

### Ventajas de Docker

- ✅ No necesitas instalar PostgreSQL manualmente
- ✅ Entorno consistente entre desarrollo y producción
- ✅ Fácil de configurar y ejecutar
- ✅ Aislamiento de dependencias

### 1. Instalar Docker

**Windows:**

- Descarga [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
- Asegúrate de habilitar WSL 2

**Linux:**

- [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Debian](https://docs.docker.com/engine/install/debian/)
- Sigue los [pasos post-instalación](https://docs.docker.com/engine/install/linux-postinstall/)

### 2. Configurar Variables de Entorno

**IMPORTANTE:** Debes crear el archivo `.env` antes de ejecutar Docker.

```bash
cp .env.example .env
```

**Genera una SECRET_KEY segura:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edita `.env` y reemplaza los valores:

```env
SECRET_KEY=pega-aqui-la-clave-generada
DEBUG=True
DATABASE_URL=postgresql://asopadel_user:password_seguro@db:5432/asopadel_barinas
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=password_seguro
```

> ⚠️ Cambia `password_seguro` por una contraseña fuerte.

### 3. Construir y Ejecutar

```bash
docker-compose up --build
```

> 💡 La primera vez tomará unos minutos mientras descarga las imágenes.

### 4. Crear Superusuario

En una **nueva terminal**:

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Acceder a la Aplicación

- **Aplicación:** [http://localhost:8000](http://localhost:8000)
- **Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)

### Comandos Útiles de Docker

```bash
# Detener contenedores
docker-compose down

# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker compose exec web python manage.py migrate

# Ejecutar comandos de Django
docker compose exec web python manage.py <comando>

# Acceder al shell de Django
docker compose exec web python manage.py shell

# Limpiar todo (⚠️ elimina la base de datos)
docker-compose down -v
```

---

## 🔒 Configuración de Seguridad

### Características de Seguridad Implementadas

1. **Variables de Entorno**
   - Todas las credenciales están en `.env`
   - No hay secretos hardcodeados en el código

2. **Rate Limiting**
   - Login limitado a 5 intentos por minuto por IP
   - Previene ataques de fuerza bruta

3. **Validación de Archivos**
   - Imágenes limitadas a 5MB
   - Solo formatos permitidos: jpg, jpeg, png, webp

4. **Sesiones Seguras**
   - Timeout de 1 hora de inactividad
   - Cookies HttpOnly y SameSite

5. **Headers de Seguridad**
   - HSTS (en producción)
   - X-Frame-Options: DENY
   - Content-Type-Nosniff

6. **Separación de Privilegios**
   - Usuarios normales no pueden modificar roles
   - Solo admins pueden gestionar permisos

### Logging de Seguridad

Los eventos de seguridad se registran en `logs/security.log`:

```bash
# Ver logs de seguridad
tail -f logs/security.log
```

---

## 🔄 Modo Desarrollo vs Producción

### Desarrollo (DEBUG=True)

```env
DEBUG=True
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Producción (DEBUG=False)

```env
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

> ⚠️ **IMPORTANTE:** En producción DEBES usar HTTPS y configurar todas las variables de seguridad.

### Checklist de Despliegue a Producción

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` única y segura (50+ caracteres)
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Contraseña de base de datos fuerte
- [ ] HTTPS habilitado
- [ ] Todas las variables de seguridad en `True`
- [ ] Archivos estáticos recolectados (`collectstatic`)
- [ ] Migraciones aplicadas
- [ ] Backup de base de datos configurado

---

## 🧪 Tests

El proyecto incluye 43+ tests automatizados.

### Ejecutar Todos los Tests

```bash
# Sin Docker
python manage.py test users --verbosity=2

# Con Docker
docker compose exec web python manage.py test users --verbosity=2
```

### Tests Específicos

```bash
# Tests de modelos
python manage.py test users.test_models

# Tests de formularios
python manage.py test users.test_forms

# Tests de vistas
python manage.py test users.test_views
```

### Verificación de Seguridad

```bash
# Verificar configuración de despliegue
python manage.py check --deploy

# Verificar problemas de seguridad
python manage.py check --deploy --fail-level WARNING
```

---

## 📝 Flujo de Trabajo Git

### Reglas Obligatorias

1. **NO trabajar directamente en `main`**
2. Seguir **GitHub Flow**
3. Crear ramas desde `main`
4. Borrar ramas después de fusionar
5. Solo fusionar si pasan los tests

### Nomenclatura de Ramas

```
feature/nombre-del-feature
bugfix/nombre-del-bugfix
security/nombre-del-fix
refactor/nombre-del-refactor
docs/nombre-de-la-documentacion
```

### Nomenclatura de Commits

```
feat: agregar nueva funcionalidad
fix: corregir bug
security: corregir vulnerabilidad
refactor: refactorizar código
docs: actualizar documentación
test: agregar o modificar tests
```

### Ejemplo de Flujo de Trabajo

```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 3. Hacer cambios y commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 4. Ejecutar tests
python manage.py test

# 5. Push a GitHub
git push origin feature/nueva-funcionalidad

# 6. Crear Pull Request en GitHub
# 7. Después de aprobación, fusionar y borrar rama
```

---

## 📚 Documentación Adicional

Para más detalles técnicos, consulta:

- [DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md) - Arquitectura y detalles técnicos
- [Reporte de Seguridad](docs/security_report.md) - Auditoría de seguridad completa

---

## 🆘 Solución de Problemas

### Error: "SECRET_KEY not found"

- Asegúrate de tener el archivo `.env` en la raíz del proyecto
- Verifica que `SECRET_KEY` esté definido en `.env`

### Error de conexión a PostgreSQL

- Verifica que PostgreSQL esté corriendo
- Confirma las credenciales en `.env`
- En Docker, asegúrate de que el contenedor `db` esté activo

### Error: "Rate limited"

- Has excedido 5 intentos de login por minuto
- Espera 1 minuto antes de intentar nuevamente

### Archivos no se suben

- Verifica que el archivo sea jpg, jpeg, png o webp
- Confirma que el tamaño sea menor a 5MB

---

## 👥 Contribuidores

- ErPyrex - Desarrollador Principal

## 📄 Licencia

Este proyecto es privado y pertenece a la Asociación de Pádel de Barinas.
