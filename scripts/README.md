# Scripts de Testing Automatizados

Este directorio contiene scripts automatizados para ejecutar tests del proyecto ASOPADEL.

## Scripts Disponibles

### 🔧 `test_all.sh` - Script Maestro

Ejecuta todos los tests del proyecto.

**Uso:**

```bash
./scripts/test_all.sh                 # Ejecutar todos los tests
./scripts/test_all.sh --backend-only  # Solo backend
./scripts/test_all.sh --frontend-only # Solo frontend
./scripts/test_all.sh --api-only      # Solo API
./scripts/test_all.sh --docker        # Incluir tests de Docker
./scripts/test_all.sh --help          # Ver ayuda
```

---

### 🐍 `test_backend.sh` - Tests de Backend

Ejecuta tests de Django con opción de coverage.

**Uso:**

```bash
./scripts/test_backend.sh
```

**Características:**

- Activa automáticamente el entorno virtual
- Ejecuta tests de Django
- Opción interactiva para coverage
- Genera reporte HTML de coverage

---

### ⚛️ `test_frontend.sh` - Tests de Frontend

Ejecuta tests de React/Vite.

**Uso:**

```bash
./scripts/test_frontend.sh
```

**Características:**

- Verifica dependencias
- Ejecuta tests con Vitest
- Opción para coverage
- Reporte de cobertura

---

### 🌐 `test_api.sh` - Tests de Integración API

Prueba endpoints de la API REST con curl.

**Uso:**

```bash
./scripts/test_api.sh
```

**Tests incluidos:**

- ✅ API Root accesible
- ✅ Listar torneos
- ✅ Listar canchas
- ✅ Listar partidos
- ✅ Login con credenciales inválidas
- ✅ Endpoints protegidos requieren auth
- ✅ Crear recursos sin auth falla

---

### 🐳 `test_docker.sh` - Tests de Docker

Verifica que todos los servicios Docker funcionen correctamente.

**Uso:**

```bash
./scripts/test_docker.sh
```

**Tests incluidos:**

- ✅ Contenedores corriendo
- ✅ Backend health check
- ✅ Conexión a base de datos
- ✅ Tests de Django en Docker
- ✅ Frontend accesible
- ✅ API respondiendo
- ✅ Integridad de base de datos

---

## Ejemplos de Uso

### Desarrollo Local

```bash
# Tests rápidos durante desarrollo
./scripts/test_backend.sh

# Tests de API
./scripts/test_api.sh
```

### Pre-commit

```bash
# Ejecutar todos los tests antes de commit
./scripts/test_all.sh
```

### CI/CD

```bash
# En pipeline de CI/CD
./scripts/test_all.sh --docker
```

### Solo un tipo de test

```bash
# Backend
./scripts/test_all.sh --backend-only

# Frontend
./scripts/test_all.sh --frontend-only

# API
./scripts/test_all.sh --api-only
```

---

## Requisitos

### Para tests locales

- Python 3.10+ con venv
- Node.js 20+
- PostgreSQL (si no usa Docker)

### Para tests con Docker

- Docker Engine
- Docker Compose

---

## Salida de Ejemplo

```
==========================================
  ASOPADEL - Complete Test Suite
==========================================

==========================================
Running: Backend Tests
==========================================
✓ Virtual environment active

Running Django tests...
------------------------
...
✅ Backend Tests: PASSED

==========================================
Running: Frontend Tests
==========================================
✓ Dependencies installed

Running React tests...
----------------------
...
✅ Frontend Tests: PASSED

==========================================
  FINAL TEST SUMMARY
==========================================
Total Test Suites:  2
Passed:             2
Failed:             0
==========================================

✅ All test suites passed!
```

---

## Integración con Git Hooks

Agregar a `.git/hooks/pre-commit`:

```bash
#!/bin/bash
./scripts/test_all.sh --backend-only --api-only
```

---

## Troubleshooting

### "Permission denied"

```bash
chmod +x scripts/*.sh
```

### "Virtual environment not found"

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "API not running"

```bash
# Iniciar servidor
python manage.py runserver
# O con Docker
docker compose up
```
