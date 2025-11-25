# Solución al Error de Autenticación de PostgreSQL en Docker

## Problema

```
FATAL: password authentication failed for user "asopadel_user"
Role "asopadel_user" does not exist.
```

## Causa

Las credenciales en el archivo `.env` no son consistentes:

- `DATABASE_URL` tiene: `user:password@localhost`
- `POSTGRES_USER` tiene: `asopadel_user`
- `POSTGRES_PASSWORD` tiene: `12341234.`

Docker crea el usuario PostgreSQL con `POSTGRES_USER` y `POSTGRES_PASSWORD`, pero Django intenta conectarse con las credenciales de `DATABASE_URL`.

## Solución

### Opción 1: Actualizar tu archivo .env (Recomendado)

Edita tu archivo `.env` y asegúrate de que las credenciales coincidan:

```env
# Django Configuration
SECRET_KEY=3k35cog13#x53j3dn1ab5nf^1#k=%&t5bv2*wxh0d9k&p6nm20
DEBUG=True

# Database Configuration
# IMPORTANTE: El usuario y contraseña deben coincidir con POSTGRES_USER y POSTGRES_PASSWORD
DATABASE_URL=postgresql://asopadel_user:12341234.@db:5432/asopadel_barinas

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Configuration (for Docker)
POSTGRES_DB=asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=12341234.

# Security Settings (Development)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Cambios necesarios:**

1. En `DATABASE_URL`, cambiar `user:password@localhost` por `asopadel_user:12341234.@db`
2. Cambiar `localhost` por `db` (nombre del servicio Docker)

### Opción 2: Limpiar y Reconstruir

Si ya ejecutaste Docker antes:

```bash
# 1. Detener y eliminar contenedores y volúmenes
docker-compose down -v

# 2. Actualizar tu .env como se indica arriba

# 3. Reconstruir y ejecutar
docker-compose up --build
```

### Verificar que Funciona

Deberías ver:

```
web-1  | Operations to perform:
web-1  |   Apply all migrations: ...
web-1  | Running migrations:
web-1  |   Applying contenttypes.0001_initial... OK
web-1  |   ...
```

## Prevención

Siempre asegúrate de que:

1. `DATABASE_URL` use el mismo usuario que `POSTGRES_USER`
2. `DATABASE_URL` use la misma contraseña que `POSTGRES_PASSWORD`
3. `DATABASE_URL` use `db` como host (no `localhost`) cuando uses Docker
4. Las credenciales sean seguras (no uses `password` o `12341234.` en producción)

## Archivo .env.example Actualizado

El archivo `.env.example` ahora tiene las credenciales correctas y consistentes.
