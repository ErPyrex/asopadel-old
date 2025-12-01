# Guía de Migración: Django Templates → React/Vite Frontend

## Índice

1. [Arquitectura Propuesta](#arquitectura-propuesta)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Migración del Backend](#migración-del-backend)
4. [Creación del Frontend](#creación-del-frontend)
5. [Modificación del Diseño](#modificación-del-diseño)
6. [Despliegue](#despliegue)

---

## Arquitectura Propuesta

### Estructura del Proyecto

```
asopadel/
├── backend/                    # Django (API REST)
│   ├── asopadel_barinas/      # Configuración
│   ├── users/                 # App usuarios
│   ├── competitions/          # App torneos
│   ├── facilities/            # App canchas
│   ├── blog/                  # App noticias
│   └── api/                   # Endpoints REST (NUEVO)
│
├── frontend/                   # React + Vite (NUEVO)
│   ├── src/
│   │   ├── components/        # Componentes reutilizables
│   │   ├── pages/            # Páginas/Vistas
│   │   ├── services/         # Llamadas API
│   │   ├── hooks/            # Custom hooks
│   │   ├── context/          # Estado global
│   │   └── assets/           # Imágenes, estilos
│   ├── public/
│   └── package.json
│
└── docker-compose.yml         # Orquestación (actualizado)
```

### Flujo de Comunicación

```
Usuario → React (Puerto 5173) → API REST (Puerto 8000) → PostgreSQL
         ↓
    Renderiza UI
```

---

## Instalación y Configuración

### Paso 1: Instalar Django REST Framework

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate  # Windows

# Instalar DRF y CORS
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
pip freeze > requirements.txt
```

### Paso 2: Configurar Django para API

**`asopadel_barinas/settings.py`:**

```python
INSTALLED_APPS = [
    # ... apps existentes
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Debe estar primero
    'django.middleware.security.SecurityMiddleware',
    # ... resto del middleware
]

# Configuración CORS (desarrollo)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

# Configuración REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### Paso 3: Crear API Endpoints

**Crear `api/` app:**

```bash
python manage.py startapp api
```

**`api/serializers.py`:**

```python
from rest_framework import serializers
from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'cedula', 'email', 'first_name', 'last_name', 
                  'telefono', 'foto', 'es_admin_aso', 'es_arbitro', 'es_jugador']
        read_only_fields = ['es_admin_aso', 'es_arbitro', 'es_jugador']

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = '__all__'

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'
```

**`api/views.py`:**

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Usuario
from competitions.models import Torneo, Partido
from facilities.models import Cancha
from .serializers import (
    UsuarioSerializer, TorneoSerializer, 
    PartidoSerializer, CanchaSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class TorneoViewSet(viewsets.ModelViewSet):
    queryset = Torneo.objects.all()
    serializer_class = TorneoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CanchaViewSet(viewsets.ModelViewSet):
    queryset = Cancha.objects.all()
    serializer_class = CanchaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

**`api/urls.py`:**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UsuarioViewSet, TorneoViewSet, PartidoViewSet, CanchaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'torneos', TorneoViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'canchas', CanchaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**`asopadel_barinas/urls.py`:**

```python
urlpatterns = [
    # ... URLs existentes
    path('api/', include('api.urls')),  # NUEVO
]
```

---

## Creación del Frontend

### Paso 1: Crear Proyecto Vite + React

```bash
# Desde la raíz del proyecto
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

### Paso 2: Instalar Dependencias

```bash
npm install axios react-router-dom @tanstack/react-query
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Paso 3: Configurar Tailwind CSS

**`frontend/tailwind.config.js`:**

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**`frontend/src/index.css`:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Paso 4: Configurar Axios

**`frontend/src/services/api.js`:**

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para refrescar token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

### Paso 5: Crear Servicios

**`frontend/src/services/authService.js`:**

```javascript
import api from './api';

export const authService = {
  login: async (cedula, password) => {
    const response = await api.post('/token/', { cedula, password });
    const { access, refresh } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: async () => {
    const response = await api.get('/usuarios/me/');
    return response.data;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};
```

**`frontend/src/services/torneoService.js`:**

```javascript
import api from './api';

export const torneoService = {
  getAll: async () => {
    const response = await api.get('/torneos/');
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/torneos/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/torneos/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/torneos/${id}/`, data);
    return response.data;
  },

  delete: async (id) => {
    await api.delete(`/torneos/${id}/`);
  },
};
```

### Paso 6: Crear Componentes

**`frontend/src/components/Navbar.jsx`:**

```jsx
import { Link } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Navbar({ user }) {
  const handleLogout = () => {
    authService.logout();
    window.location.href = '/login';
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">
          ASOPADEL
        </Link>
        
        <div className="flex gap-4">
          <Link to="/torneos" className="hover:text-blue-200">
            Torneos
          </Link>
          <Link to="/canchas" className="hover:text-blue-200">
            Canchas
          </Link>
          
          {user ? (
            <>
              <Link to="/perfil" className="hover:text-blue-200">
                {user.first_name}
              </Link>
              <button onClick={handleLogout} className="hover:text-blue-200">
                Salir
              </button>
            </>
          ) : (
            <Link to="/login" className="hover:text-blue-200">
              Iniciar Sesión
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
```

**`frontend/src/pages/Login.jsx`:**

```jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/authService';

export default function Login() {
  const [cedula, setCedula] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await authService.login(cedula, password);
      navigate('/');
    } catch (err) {
      setError('Cédula o contraseña incorrecta');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Iniciar Sesión</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Cédula</label>
            <input
              type="text"
              value={cedula}
              onChange={(e) => setCedula(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 mb-2">Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
}
```

**`frontend/src/pages/Torneos.jsx`:**

```jsx
import { useQuery } from '@tanstack/react-query';
import { torneoService } from '../services/torneoService';

export default function Torneos() {
  const { data: torneos, isLoading, error } = useQuery({
    queryKey: ['torneos'],
    queryFn: torneoService.getAll,
  });

  if (isLoading) return <div className="text-center py-8">Cargando...</div>;
  if (error) return <div className="text-center py-8 text-red-600">Error al cargar torneos</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Torneos</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {torneos?.results?.map((torneo) => (
          <div key={torneo.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <h3 className="text-xl font-semibold mb-2">{torneo.nombre}</h3>
            <p className="text-gray-600 mb-4">{torneo.descripcion}</p>
            <div className="flex justify-between text-sm text-gray-500">
              <span>Inicio: {new Date(torneo.fecha_inicio).toLocaleDateString()}</span>
              <span className="capitalize">{torneo.estado}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Paso 7: Configurar Rutas

**`frontend/src/App.jsx`:**

```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Torneos from './pages/Torneos';
import { authService } from './services/authService';

const queryClient = new QueryClient();

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (authService.isAuthenticated()) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          authService.logout();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  if (loading) return <div>Cargando...</div>;

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Navbar user={user} />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/torneos" element={<Torneos />} />
          <Route path="/" element={<Navigate to="/torneos" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

---

## Modificación del Diseño

### Dónde Modificar Estilos

1. **Tailwind CSS (Recomendado):**
   - Modificar clases directamente en componentes JSX
   - Personalizar `tailwind.config.js` para colores, fuentes, etc.

2. **CSS Modules:**

   ```jsx
   // Component.module.css
   .card {
     background: white;
     border-radius: 8px;
   }
   
   // Component.jsx
   import styles from './Component.module.css';
   <div className={styles.card}>...</div>
   ```

3. **Styled Components:**

   ```bash
   npm install styled-components
   ```

   ```jsx
   import styled from 'styled-components';
   
   const Card = styled.div`
     background: white;
     border-radius: 8px;
     padding: 1rem;
   `;
   ```

### Ejemplo de Personalización

**`frontend/tailwind.config.js`:**

```javascript
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          700: '#1d4ed8',
        },
        secondary: '#10b981',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

---

## Despliegue

### Docker Compose Actualizado

**`docker-compose.yml`:**

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=asopadel_barinas
      - POSTGRES_USER=asopadel_user
      - POSTGRES_PASSWORD=postgres

  backend:
    build: .
    command: gunicorn asopadel_barinas.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000/api

volumes:
  postgres_data:
```

**`frontend/Dockerfile`:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
```

---

## Ventajas de esta Arquitectura

✅ **Separación de responsabilidades**: Backend y frontend independientes  
✅ **Mejor UX**: Aplicación de página única (SPA) más rápida  
✅ **Escalabilidad**: Puedes escalar backend y frontend por separado  
✅ **Reutilización**: La API puede usarse para apps móviles  
✅ **Desarrollo paralelo**: Equipos pueden trabajar independientemente  
✅ **Tecnologías modernas**: React, Vite, Tailwind CSS  

---

## Próximos Pasos

1. ✅ Configurar Django REST Framework
2. ✅ Crear endpoints API
3. ✅ Crear proyecto React + Vite
4. ✅ Implementar autenticación JWT
5. ✅ Migrar vistas una por una
6. ✅ Actualizar Docker Compose
7. ✅ Desplegar en producción

¿Quieres que implemente alguna parte específica de esta migración?
