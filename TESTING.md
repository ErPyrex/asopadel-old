# Guía de Testing - ASOPADEL

## 📋 Índice

1. [Testing del Backend (API)](#testing-del-backend-api)
2. [Testing del Frontend (React)](#testing-del-frontend-react)
3. [Testing de Integración](#testing-de-integración)
4. [Testing con Docker](#testing-con-docker)
5. [Testing Manual](#testing-manual)

---

## Testing del Backend (API)

### Configuración de Tests

Django incluye un framework de testing integrado. Los tests se encuentran en archivos `tests.py` o `test_*.py`.

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test api

# Test específico
python manage.py test api.tests.TestUsuarioViewSet

# Con verbosidad
python manage.py test --verbosity=2

# Mantener base de datos de test
python manage.py test --keepdb
```

### Ejemplo de Tests para API

**Crear `api/tests.py`:**

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Usuario

class TestAuthenticationAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Usuario.objects.create_user(
            cedula='12345678',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
    
    def test_login_success(self):
        """Test login con credenciales correctas"""
        response = self.client.post('/api/auth/login/', {
            'cedula': '12345678',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login con credenciales incorrectas"""
        response = self.client.post('/api/auth/login/', {
            'cedula': '12345678',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestTorneoAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Usuario.objects.create_user(
            cedula='12345678',
            password='testpass123'
        )
        # Login y obtener token
        response = self.client.post('/api/auth/login/', {
            'cedula': '12345678',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_list_torneos(self):
        """Test listar torneos"""
        response = self.client.get('/api/torneos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_torneo_unauthorized(self):
        """Test crear torneo sin permisos de admin"""
        self.client.credentials()  # Remove auth
        response = self.client.post('/api/torneos/', {
            'nombre': 'Test Torneo',
            'descripcion': 'Test',
            'fecha_inicio': '2025-01-01',
            'fecha_fin': '2025-01-31'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### Tests de Modelos

```python
from django.test import TestCase
from users.models import Usuario

class TestUsuarioModel(TestCase):
    def test_create_user(self):
        """Test crear usuario"""
        user = Usuario.objects.create_user(
            cedula='12345678',
            password='testpass123',
            email='test@example.com'
        )
        self.assertEqual(user.cedula, '12345678')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_str(self):
        """Test representación string del usuario"""
        user = Usuario.objects.create_user(
            cedula='12345678',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(str(user), 'John Doe')
```

---

## Testing del Frontend (React)

### Configuración

El proyecto usa Vite que incluye Vitest para testing.

**Instalar dependencias:**

```bash
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

**Configurar `vite.config.js`:**

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
```

**Crear `frontend/src/test/setup.js`:**

```javascript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

### Ejemplo de Tests

**Test de Componente - `Login.test.jsx`:**

```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../pages/Login';
import { authService } from '../services/authService';

vi.mock('../services/authService');

describe('Login Component', () => {
  it('renders login form', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Iniciar Sesión')).toBeInTheDocument();
    expect(screen.getByLabelText('Cédula')).toBeInTheDocument();
    expect(screen.getByLabelText('Contraseña')).toBeInTheDocument();
  });
  
  it('handles successful login', async () => {
    authService.login.mockResolvedValue({ id: 1, cedula: '12345678' });
    
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    fireEvent.change(screen.getByLabelText('Cédula'), {
      target: { value: '12345678' }
    });
    fireEvent.change(screen.getByLabelText('Contraseña'), {
      target: { value: 'testpass' }
    });
    fireEvent.click(screen.getByText('Ingresar'));
    
    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith('12345678', 'testpass');
    });
  });
});
```

**Test de Servicio - `authService.test.js`:**

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { authService } from '../services/authService';

describe('authService', () => {
  beforeEach(() => {
    localStorage.clear();
  });
  
  it('stores tokens on login', async () => {
    const mockResponse = {
      access: 'access_token',
      refresh: 'refresh_token',
      user: { id: 1, cedula: '12345678' }
    };
    
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })
    );
    
    await authService.login('12345678', 'password');
    
    expect(localStorage.getItem('access_token')).toBe('access_token');
    expect(localStorage.getItem('refresh_token')).toBe('refresh_token');
  });
  
  it('clears tokens on logout', () => {
    localStorage.setItem('access_token', 'token');
    localStorage.setItem('refresh_token', 'refresh');
    
    authService.logout();
    
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('refresh_token')).toBeNull();
  });
});
```

### Ejecutar Tests Frontend

```bash
cd frontend

# Ejecutar tests
npm run test

# Watch mode
npm run test -- --watch

# Coverage
npm run test -- --coverage
```

---

## Testing de Integración

### Con curl

**Test de Login:**

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"cedula":"12345678","password":"testpass"}'

# Respuesta esperada:
# {"access":"...","refresh":"...","user":{...}}
```

**Test de Endpoints Protegidos:**

```bash
# Guardar token
TOKEN="tu_access_token_aqui"

# Listar torneos
curl http://localhost:8000/api/torneos/ \
  -H "Authorization: Bearer $TOKEN"

# Crear torneo (solo admin)
curl -X POST http://localhost:8000/api/torneos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Torneo Test",
    "descripcion": "Descripción",
    "fecha_inicio": "2025-01-01",
    "fecha_fin": "2025-01-31",
    "estado": "programado"
  }'
```

### Con Postman/Insomnia

1. **Importar Collection:**
   - Crear colección "ASOPADEL API"
   - Configurar base URL: `http://localhost:8000/api`

2. **Configurar Autenticación:**
   - Request: POST `/auth/login/`
   - Body: `{"cedula":"...","password":"..."}`
   - Guardar token en variable de entorno

3. **Tests de Endpoints:**
   - GET `/torneos/` - Lista
   - POST `/torneos/` - Crear
   - GET `/torneos/{id}/` - Detalle
   - PUT `/torneos/{id}/` - Actualizar
   - DELETE `/torneos/{id}/` - Eliminar

---

## Testing con Docker

### Tests del Backend en Docker

```bash
# Ejecutar tests
docker compose exec backend python manage.py test

# Con coverage
docker compose exec backend coverage run --source='.' manage.py test
docker compose exec backend coverage report
```

### Verificar Servicios

```bash
# Estado de contenedores
docker compose ps

# Logs del backend
docker compose logs backend

# Logs del frontend
docker compose logs frontend

# Verificar base de datos
docker compose exec db psql -U asopadel_user -d asopadel_barinas -c "SELECT COUNT(*) FROM users_usuario;"
```

### Health Checks

**Agregar a `docker-compose.yml`:**

```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  
  frontend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5173/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Testing Manual

### Checklist de Funcionalidades

#### Autenticación

- [ ] Login con credenciales correctas
- [ ] Login con credenciales incorrectas
- [ ] Logout
- [ ] Token refresh automático
- [ ] Redirección a login si no autenticado

#### Navegación

- [ ] Página de inicio pública accesible
- [ ] Dashboard accesible solo autenticado
- [ ] Links del navbar funcionan
- [ ] Logout redirige a home

#### Torneos

- [ ] Listar torneos
- [ ] Ver detalle de torneo
- [ ] Crear torneo (solo admin)
- [ ] Editar torneo (solo admin)
- [ ] Eliminar torneo (solo admin)

#### Canchas

- [ ] Listar canchas
- [ ] Ver disponibilidad
- [ ] Reservar cancha (autenticado)

#### Usuarios (Solo Admin)

- [ ] Listar usuarios
- [ ] Ver roles de usuarios
- [ ] Filtrar por rol

#### Partidos

- [ ] Listar partidos
- [ ] Ver estado de partidos
- [ ] Filtrar por torneo

### Tests de Responsividad

- [ ] Mobile (< 768px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (> 1024px)

### Tests de Navegadores

- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari

### Tests de Rendimiento

```bash
# Lighthouse (Chrome DevTools)
# - Performance
# - Accessibility
# - Best Practices
# - SEO

# Backend response time
curl -w "@-" -o /dev/null -s http://localhost:8000/api/torneos/ <<'EOF'
    time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
      time_redirect:  %{time_redirect}\n
   time_pretransfer:  %{time_pretransfer}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
EOF
```

---

## Automatización de Tests

### GitHub Actions

**Crear `.github/workflows/test.yml`:**

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm run test
```

---

## Métricas de Calidad

### Coverage Mínimo Recomendado

- **Backend:** 80%
- **Frontend:** 70%
- **Integración:** 60%

### Herramientas

- **Backend:** `coverage.py`
- **Frontend:** Vitest coverage
- **E2E:** Playwright/Cypress

---

## Próximos Pasos

1. Implementar tests unitarios para todos los ViewSets
2. Agregar tests de componentes React
3. Configurar CI/CD con GitHub Actions
4. Implementar tests E2E con Playwright
5. Monitoreo de performance en producción
