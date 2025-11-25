# Configuración Local - Paso a Paso

## Estado Actual

- ✅ PostgreSQL está corriendo
- ✅ Python 3.12.3 instalado
- ✅ Django 5.0.1 en venv
- ❌ `.env` configurado para Docker (usa `@db`)

## Pasos para Ejecutar Localmente

### Paso 1: Actualizar .env

Edita el archivo `.env` y cambia la línea de `DATABASE_URL`:

**Antes:**

```
DATABASE_URL=postgresql://asopadel_user:postgres@db:5432/asopadel_barinas
```

**Después:**

```
DATABASE_URL=postgresql://asopadel_user:postgres@localhost:5432/asopadel_barinas
```

**Comando rápido:**

```bash
sed -i 's|@db:|@localhost:|g' .env
```

### Paso 2: Configurar PostgreSQL

Ejecuta estos comandos:

```bash
sudo -u postgres psql
```

Dentro de psql, ejecuta:

```sql
-- Crear base de datos
CREATE DATABASE asopadel_barinas;

-- Crear usuario
CREATE USER asopadel_user WITH PASSWORD 'postgres';

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
ALTER ROLE asopadel_user SET client_encoding TO 'utf8';
ALTER ROLE asopadel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE asopadel_user SET timezone TO 'America/Caracas';

-- Conectar a la base de datos
\c asopadel_barinas

-- Otorgar permisos en el schema (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO asopadel_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO asopadel_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO asopadel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO asopadel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO asopadel_user;

-- Salir
\q
```

### Paso 3: Activar Entorno Virtual

```bash
source venv/bin/activate
```

### Paso 4: Aplicar Migraciones

```bash
python manage.py migrate
```

Deberías ver:

```
Operations to perform:
  Apply all migrations: admin, auth, blog, competitions, contenttypes, facilities, sessions, store, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

### Paso 5: Crear Superusuario

```bash
python manage.py createsuperuser
```

Ingresa:

- Cédula: (tu número de identificación)
- Email: (tu correo)
- Nombre y Apellido
- Contraseña

### Paso 6: Ejecutar Servidor

```bash
python manage.py runserver
```

Deberías ver:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Paso 7: Acceder

Abre tu navegador en: <http://localhost:8000>

---

## Comandos Rápidos (Todo en Uno)

Si ya configuraste PostgreSQL, puedes ejecutar:

```bash
# 1. Actualizar .env
sed -i 's|@db:|@localhost:|g' .env

# 2. Activar venv
source venv/bin/activate

# 3. Aplicar migraciones
python manage.py migrate

# 4. Ejecutar servidor
python manage.py runserver
```

---

## Solución de Problemas

### Error: "role asopadel_user does not exist"

Ejecuta en psql:

```sql
CREATE USER asopadel_user WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
```

### Error: "database asopadel_barinas does not exist"

Ejecuta en psql:

```sql
CREATE DATABASE asopadel_barinas;
```

### Error: "permission denied for schema public"

Ejecuta en psql (conectado a asopadel_barinas):

```sql
\c asopadel_barinas
GRANT ALL ON SCHEMA public TO asopadel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO asopadel_user;
```

### Error: "Permission denied: logs/security.log"

Este error ocurre cuando Docker creó el archivo con permisos de root. Solución:

```bash
rm -f logs/security.log
touch logs/security.log
```

O si necesitas sudo:

```bash
sudo rm -f logs/security.log
touch logs/security.log
```

### Error: "ModuleNotFoundError"

Activa el entorno virtual:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Volver a Docker

Si quieres volver a usar Docker, cambia `.env`:

```bash
sed -i 's|@localhost:|@db:|g' .env
```

Luego:

```bash
docker compose up --build
```
