# ASOPADEL

Sistema de Gestión para la Asociación de Pádel de Barinas

---

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/ErPyrex/asopadel.git
cd asopadel

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu SECRET_KEY (genera una con el comando abajo)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Ejecutar con Docker
docker compose up --build

# 4. Crear superusuario (en otra terminal)
docker compose exec web python manage.py createsuperuser

# 5. Acceder
# http://localhost:8000
```

### Opción 2: Python Local

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/ErPyrex/asopadel.git
cd asopadel

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Edita .env: cambia @db por @localhost y agrega SECRET_KEY

# 5. Configurar PostgreSQL
sudo -u postgres psql
```

```sql
CREATE DATABASE asopadel_barinas;
CREATE USER asopadel_user WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE asopadel_barinas TO asopadel_user;
\c asopadel_barinas
GRANT ALL ON SCHEMA public TO asopadel_user;
\q
```

```bash
# 6. Aplicar migraciones
python manage.py migrate

# 7. Crear superusuario
python manage.py createsuperuser

# 8. Ejecutar servidor
python manage.py runserver
```

---

## 📋 Requisitos

### Docker

- Docker Engine
- Docker Compose v2

### Python Local

- Python 3.10+
- PostgreSQL 16
- Git

---

## 🔧 Comandos Útiles

### Docker

```bash
# Ver logs
docker compose logs -f web

# Detener
docker compose down

# Limpiar todo (⚠️ elimina datos)
docker compose down -v

# Ejecutar comandos Django
docker compose exec web python manage.py <comando>

# Acceder a PostgreSQL
docker compose exec db psql -U asopadel_user -d asopadel_barinas
```

### Python Local

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

## ⚠️ Solución de Problemas Comunes

### "docker-compose: command not found"

Usa `docker compose` (con espacio) en lugar de `docker-compose`.

### "password authentication failed"

Verifica que las credenciales en `.env` coincidan:

```env
DATABASE_URL=postgresql://asopadel_user:postgres@db:5432/asopadel_barinas
POSTGRES_USER=asopadel_user
POSTGRES_PASSWORD=postgres
```

### "Permission denied: logs/security.log"

```bash
rm -f logs/security.log
touch logs/security.log
```

### "connection refused" a PostgreSQL

**Docker:** `docker compose ps` - Verifica que 'db' esté running  
**Local:** `sudo systemctl start postgresql`

### Cambiar entre Docker y Local

**Para Docker:** `sed -i 's|@localhost:|@db:|g' .env`  
**Para Local:** `sed -i 's|@db:|@localhost:|g' .env`

---

## 🔒 Seguridad

El proyecto implementa:

- ✅ Variables de entorno para secretos
- ✅ Rate limiting (5 intentos/minuto en login)
- ✅ Validación de archivos (5MB máx, solo imágenes)
- ✅ Separación de privilegios
- ✅ Headers de seguridad HTTP
- ✅ Sesiones seguras (timeout 1 hora)
- ✅ Logging de eventos de seguridad

**Importante:**

- Nunca subas el archivo `.env` a Git
- Usa contraseñas fuertes en producción
- Configura `DEBUG=False` en producción
- Habilita HTTPS en producción

---

## 📚 Documentación

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
