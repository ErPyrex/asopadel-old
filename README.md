# ASOPADEL - React/Vite Frontend + Django REST API

Sistema de Gestión para la Asociación de Pádel de Barinas con arquitectura moderna de frontend/backend separados.

---

## 🏗️ Arquitectura

**Frontend:** React + Vite + Tailwind CSS (Puerto 5173)  
**Backend:** Django REST Framework + PostgreSQL (Puerto 8000)  
**Comunicación:** API REST con autenticación JWT

```
┌─────────────┐      HTTP/JSON      ┌──────────────┐      ┌────────────┐
│   React     │ ◄──────────────────► │   Django     │ ◄───►│ PostgreSQL │
│   (Vite)    │    JWT Tokens       │   REST API   │      │            │
└─────────────┘                      └──────────────┘      └────────────┘
  Port 5173                            Port 8000
```

---

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar el proyecto
git clone https://github.com/ErPyrex/asopadel.git
cd asopadel

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu SECRET_KEY

# 3. Iniciar todos los servicios
docker compose up --build

# 4. Crear superusuario (en otra terminal)
docker compose exec backend python manage.py createsuperuser

# 5. Acceder
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

### Opción 2: Desarrollo Local

#### Backend (Django)

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Edita .env: cambia @db por @localhost y agrega SECRET_KEY

# 4. Configurar PostgreSQL
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
# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor backend
python manage.py runserver
```

#### Frontend (React/Vite)

```bash
# 1. Ir al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.example .env
# El archivo ya tiene: VITE_API_URL=http://localhost:8000/api

# 4. Ejecutar servidor frontend
npm run dev

# 5. Acceder: http://localhost:5173
```

---

## 🔄 Actualizar Proyecto Existente y Ejecutar

Si ya tienes el repositorio clonado y quieres actualizarlo a los últimos cambios:

### Con Docker (Recomendado para Windows)

```bash
# 1. Navegar al directorio del proyecto
cd ruta/al/proyecto/asopadel

# 2. Obtener últimos cambios
git pull origin main
# O si trabajas en la rama de migración:
git pull origin feature/react-vite-migration

# 3. Reconstruir e iniciar servicios
docker compose down
docker compose up --build

# 4. Si hay nuevas migraciones, aplicarlas
docker compose exec backend python manage.py migrate

# ✅ Listo! Accede a http://localhost:5173
```

### Sin Docker (Desarrollo Local)

```bash
# 1. Actualizar código
git pull origin main

# 2. Backend - Actualizar dependencias y migraciones
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # En terminal 1

# 3. Frontend - Actualizar dependencias
cd frontend
npm install
npm run dev  # En terminal 2

# ✅ Listo! Accede a http://localhost:5173
```

### Notas para Colaboradores en Windows

**Requisitos:**

- Docker Desktop para Windows (<https://www.docker.com/products/docker-desktop/>)
- Git para Windows (<https://git-scm.com/download/win>)

**Comandos en PowerShell:**

```powershell
# Clonar (primera vez)
git clone https://github.com/ErPyrex/asopadel.git
cd asopadel

# Copiar variables de entorno
copy .env.example .env

# Iniciar con Docker
docker compose up --build

# Crear superusuario (en otra terminal)
docker compose exec backend python manage.py createsuperuser
```

**Flujo de trabajo diario:**

```powershell
# Al empezar
git pull
docker compose up

# Al terminar
git add .
git commit -m "descripción de cambios"
git push
docker compose stop
```

---

## 📋 Requisitos

### Docker

- Docker Engine 20.10+
- Docker Compose v2.0+

### Desarrollo Local

- **Backend:** Python 3.10+, PostgreSQL 16
- **Frontend:** Node.js 18+, npm 9+
- Git

---

## 🔧 Comandos Útiles

### Docker

```bash
# Ver logs
docker compose logs -f backend
docker compose logs -f frontend

# Reiniciar servicios
docker compose restart backend
docker compose restart frontend

# Detener todo
docker compose down

# Limpiar volúmenes (⚠️ elimina datos)
docker compose down -v

# Ejecutar comandos Django
docker compose exec backend python manage.py <comando>

# Acceder a PostgreSQL
docker compose exec db psql -U asopadel_user -d asopadel_barinas
```

### Backend Local

```bash
# Activar entorno virtual
source venv/bin/activate

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test

# Shell interactivo
python manage.py shell
```

### Frontend Local

```bash
cd frontend

# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview de producción
npm run preview

# Linting
npm run lint
```

---

## 🔒 Seguridad

### Características Implementadas

- ✅ JWT Authentication (tokens de acceso y refresh)
- ✅ CORS configurado para frontend
- ✅ Rate limiting en endpoints críticos
- ✅ Validación de archivos (5MB máx, solo imágenes)
- ✅ Separación de privilegios
- ✅ Headers de seguridad HTTP
- ✅ Sesiones seguras
- ✅ Logging de eventos de seguridad

### Configuración de Producción

**Backend (.env):**

```env
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
SECRET_KEY=<clave-segura-aleatoria>
SECURE_SSL_REDIRECT=True
```

**Frontend (.env):**

```env
VITE_API_URL=https://api.tudominio.com/api
```

---

## 📚 Documentación

- **[DOCUMENTACION_TECNICA.md](DOCUMENTACION_TECNICA.md)** - Arquitectura completa, modelos, API endpoints
- **[FRONTEND_MIGRATION_GUIDE.md](FRONTEND_MIGRATION_GUIDE.md)** - Guía detallada de la migración a React/Vite
- **API Docs:** <http://localhost:8000/api/> (cuando el servidor está corriendo)

---

## 🎨 Modificar el Diseño

El frontend usa **Tailwind CSS** para estilos. Para modificar el diseño:

### Cambiar Colores

Edita `frontend/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#3b82f6',  // Tu color principal
        600: '#2563eb',
      },
    },
  },
}
```

### Modificar Componentes

Los componentes están en `frontend/src/components/`:

```jsx
// Ejemplo: frontend/src/components/Navbar.jsx
<nav className="bg-primary-600 text-white shadow-lg">
  {/* Cambia las clases de Tailwind directamente */}
</nav>
```

### Crear Nuevos Componentes

```bash
# Crear nuevo componente
touch frontend/src/components/MiComponente.jsx
```

```jsx
export default function MiComponente() {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      {/* Tu contenido */}
    </div>
  );
}
```

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
python manage.py test  # Backend
cd frontend && npm run lint  # Frontend

# 4. Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

---

## ⚠️ Solución de Problemas

### "CORS error" en el frontend

Verifica que el backend tenga configurado CORS:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
```

### "401 Unauthorized" en requests

El token JWT expiró. Cierra sesión y vuelve a iniciar sesión.

### Frontend no se conecta al backend

Verifica la variable de entorno:

```bash
# frontend/.env
VITE_API_URL=http://localhost:8000/api
```

### Docker: "port already in use"

```bash
# Detener servicios que usan los puertos
docker compose down
# O cambiar puertos en docker-compose.yml
```

---

## 📄 Licencia

Proyecto privado - Asociación de Pádel de Barinas

---

## 🆘 Soporte

Para problemas o preguntas:

- Consulta la [documentación técnica](DOCUMENTACION_TECNICA.md)
- Revisa la [guía de migración](FRONTEND_MIGRATION_GUIDE.md)
- Abre un issue en GitHub
