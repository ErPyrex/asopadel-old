# Guía de Ejecución - ASOPADEL

## 🐳 Método 1: Docker (Recomendado)

### Paso 1: Limpiar instalación anterior (si existe)

```bash
docker compose down -v
```

### Paso 2: Verificar archivo .env

Tu archivo `.env` actual está correcto. Verifica que tenga:

```env
DATABASE_URL=postgresql://asopadel_user:postgres@db:5432/asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=postgres
```

### Paso 3: Construir y ejecutar

```bash
docker compose up --build
```

Deberías ver:

```
✅ Container asopadel-db-1    Created
✅ Container asopadel-web-1   Created
```

### Paso 4: Crear superusuario (en otra terminal)

```bash
docker compose exec web python manage.py createsuperuser
```

### Paso 5: Acceder

Abre tu navegador en: <http://localhost:8000>

---

## 💻 Método 2: Python Local (Sin Docker)

### Paso 1: Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Actualizar .env para local

Edita `.env` y cambia:

```env
# Cambiar 'db' por 'localhost'
DATABASE_URL=postgresql://asopadel_user:postgres@localhost:5432/asopadel_barinas
```

### Paso 4: Configurar PostgreSQL

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
\q
```

### Paso 5: Crear directorio de logs

```bash
mkdir -p logs
```

### Paso 6: Aplicar migraciones

```bash
python manage.py migrate
```

### Paso 7: Crear superusuario

```bash
python manage.py createsuperuser
```

### Paso 8: Ejecutar servidor

```bash
python manage.py runserver
```

### Paso 9: Acceder

Abre tu navegador en: <http://localhost:8000>

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

# Acceder al shell de Django
docker compose exec web python manage.py shell

# Acceder a PostgreSQL
docker compose exec db psql -U asopadel_user -d asopadel_barinas
```

### Python Local

```bash
# Activar entorno virtual
source venv/bin/activate

# Desactivar entorno virtual
deactivate

# Ver migraciones pendientes
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test users --verbosity=2

# Recolectar archivos estáticos
python manage.py collectstatic
```

---

## ❌ Solución de Problemas

### Error: "command not found: docker-compose"

Usa `docker compose` (con espacio) en lugar de `docker-compose`:

```bash
# ❌ Incorrecto
docker-compose up

# ✅ Correcto
docker compose up
```

### Error: "password authentication failed"

Verifica que las credenciales en `.env` coincidan:

```env
DATABASE_URL=postgresql://asopadel_user:postgres@db:5432/asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=postgres
```

Luego limpia y reconstruye:

```bash
docker compose down -v
docker compose up --build
```

### Error: "ModuleNotFoundError: No module named 'django'"

Activa el entorno virtual:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "port 8000 is already in use"

Detén el proceso que usa el puerto:

```bash
# Encontrar proceso
sudo lsof -i :8000

# Matar proceso (reemplaza PID)
kill -9 <PID>
```

O usa otro puerto:

```bash
python manage.py runserver 8001
```

### Error: "connection refused" a PostgreSQL

**Docker:**

```bash
docker compose ps  # Verifica que 'db' esté running
docker compose logs db  # Ver logs de PostgreSQL
```

**Local:**

```bash
sudo systemctl status postgresql  # Verificar que esté corriendo
sudo systemctl start postgresql   # Iniciar si está detenido
```

---

## 📝 Notas Importantes

1. **Docker vs Local**: No mezcles ambos métodos. Si usas Docker, el `.env` debe tener `@db`. Si usas local, debe tener `@localhost`.

2. **Entorno Virtual**: Siempre activa el entorno virtual antes de ejecutar comandos Python locales.

3. **Migraciones**: Después de cambios en modelos, ejecuta `makemigrations` y `migrate`.

4. **Seguridad**: Cambia las contraseñas por defecto (`postgres`) en producción.

5. **Logs**: Revisa `logs/security.log` para eventos de seguridad.
