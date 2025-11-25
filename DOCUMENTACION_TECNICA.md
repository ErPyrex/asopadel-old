# ASOPADEL BARINAS - Documentación Técnica Completa

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Modelos de Datos](#modelos-de-datos)
4. [Sistema de Autenticación](#sistema-de-autenticación)
5. [Roles y Permisos](#roles-y-permisos)
6. [Módulos del Sistema](#módulos-del-sistema)
7. [Flujos de Trabajo](#flujos-de-trabajo)
8. [API y Endpoints](#api-y-endpoints)
9. [Frontend y Templates](#frontend-y-templates)
10. [Tests y Calidad](#tests-y-calidad)
11. [Configuración y Despliegue](#configuración-y-despliegue)
12. [Guías de Desarrollo](#guías-de-desarrollo)

---

## Introducción

### ¿Qué es ASOPADEL BARINAS?

ASOPADEL BARINAS es un sistema web integral diseñado para la gestión de la Asociación de Pádel de Barinas. El sistema permite administrar jugadores, árbitros, torneos, canchas, noticias y toda la operación de la asociación de manera centralizada y eficiente.

### Tecnologías Utilizadas

- **Backend Framework:** Django 5.x
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **CSS Framework:** Bootstrap 5.3
- **Autenticación:** Django Authentication System (personalizado)
- **Testing:** Django TestCase
- **Servidor de Producción:** Gunicorn
- **Archivos Estáticos:** WhiteNoise

### Características Principales

✅ **Gestión de Usuarios**

- Sistema de autenticación personalizado con cédula
- Tres tipos de roles: Jugador, Árbitro, Administrador
- Gestión de perfiles con información detallada

✅ **Gestión de Torneos**

- Creación y administración de competiciones
- Seguimiento de partidos y resultados
- Rankings y estadísticas

✅ **Gestión de Instalaciones**

- Registro de canchas y facilidades
- Disponibilidad y reservas

✅ **Sistema de Noticias**

- Publicación de comunicados
- Blog de la asociación

✅ **Panel Administrativo**

- Dashboards diferenciados por rol
- Gestión centralizada de contenido
- Sistema de permisos granular

✅ **Modo Oscuro/Claro**

- Selector de tema (claro/oscuro/automático)
- Persistencia de preferencias

---

## Arquitectura del Sistema

### Estructura del Proyecto

```
asopadel/
├── asopadel_barinas/          # Configuración principal del proyecto
│   ├── settings.py            # Configuración de Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuración WSGI
│
├── users/                     # Aplicación de usuarios
│   ├── models.py              # Modelo Usuario personalizado
│   ├── views.py               # Vistas de autenticación
│   ├── forms.py               # Formularios de registro/login
│   ├── admin_management.py    # Gestión de administradores
│   ├── test_models.py         # Tests de modelos
│   ├── test_views.py          # Tests de vistas
│   └── test_forms.py          # Tests de formularios
│
├── core/                      # Aplicación principal
│   ├── models.py              # Modelos de Hero, etc.
│   ├── views.py               # Vistas principales y dashboards
│   └── urls.py                # URLs de core
│
├── competitions/              # Gestión de torneos
│   ├── models.py              # Modelos de Torneo, Partido
│   ├── views.py               # Vistas de competiciones
│   └── urls.py                # URLs de competiciones
│
├── facilities/                # Gestión de instalaciones
│   ├── models.py              # Modelo de Cancha
│   ├── views.py               # Vistas de canchas
│   └── urls.py                # URLs de facilities
│
├── blog/                      # Sistema de noticias
│   ├── models.py              # Modelo de Noticia
│   ├── views.py               # Vistas de blog
│   └── urls.py                # URLs de blog
│
├── store/                     # Tienda (futuro)
│   └── models.py              # Modelos de productos
│
├── templates/                 # Templates HTML
│   ├── base.html              # Template base
│   ├── home.html              # Página principal
│   └── users/                 # Templates de usuarios
│       ├── login.html
│       ├── register.html
│       ├── admin_management.html
│       └── panel_*.html
│
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos principales
│   └── js/
│       └── main.js            # JavaScript principal
│
├── media/                     # Archivos subidos por usuarios
│   ├── perfiles/
│   ├── noticias/
│   └── jugadores/
│
├── manage.py                  # Comando de gestión Django
├── requirements.txt           # Dependencias Python
├── run_tests.sh               # Script de ejecución de tests
└── README.md                  # Documentación básica
```

### Patrón de Diseño

El proyecto sigue el patrón **MTV (Model-Template-View)** de Django:

- **Models:** Definen la estructura de datos y lógica de negocio
- **Templates:** Presentación HTML con Django Template Language
- **Views:** Lógica de controlador que conecta modelos y templates

### Flujo de Peticiones

```
Cliente (Browser)
    ↓
URLs (asopadel_barinas/urls.py)
    ↓
View (users/views.py, core/views.py, etc.)
    ↓
Model (users/models.py, etc.)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Template (templates/*.html)
    ↓
Response (HTML/JSON)
```

---

## Modelos de Datos

### Modelo Usuario (users/models.py)

El sistema utiliza un modelo de usuario personalizado que extiende `AbstractUser`.

#### Campos Principales

```python
class Usuario(AbstractUser):
    # Identificación
    username = None  # Eliminado, se usa cedula
    cedula = models.CharField(max_length=12, unique=True)
    
    # Información Personal
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    
    # Roles
    es_admin_aso = models.BooleanField(default=False)
    es_arbitro = models.BooleanField(default=False)
    es_jugador = models.BooleanField(default=False)
    
    # Datos Adicionales
    telefono = models.CharField(max_length=20, blank=True, null=True)
    categoria_jugador = models.CharField(
        max_length=50,
        choices=[
            ('juvenil', 'Juvenil'),
            ('adulto', 'Adulto'),
            ('senior', 'Senior'),
        ],
        blank=True, null=True
    )
    ranking = models.IntegerField(default=0, blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
```

#### Manager Personalizado

```python
class UsuarioManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        """Crea un usuario regular"""
        if not cedula:
            raise ValueError("La cédula es obligatoria")
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, cedula, password=None, **extra_fields):
        """Crea un superusuario con todos los permisos"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('es_admin_aso', True)
        return self.create_user(cedula, password, **extra_fields)
```

#### Propiedades

```python
@property
def get_full_name(self):
    """Retorna nombre completo"""
    return f"{self.first_name} {self.last_name}"

@property
def get_short_name(self):
    """Retorna nombre corto"""
    return self.first_name
```

### Otros Modelos Principales

#### Hero (core/models.py)

```python
class Hero(models.Model):
    """Sección hero de la página principal"""
    titulo = models.CharField(max_length=200)
    subtitulo = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
```

#### Noticia (blog/models.py)

```python
class Noticia(models.Model):
    """Noticias y comunicados"""
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    destacada = models.BooleanField(default=False)
```

#### Cancha (facilities/models.py)

```python
class Cancha(models.Model):
    """Instalaciones deportivas"""
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('indoor', 'Interior'),
            ('outdoor', 'Exterior'),
        ]
    )
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='canchas/', blank=True, null=True)
```

#### Torneo (competitions/models.py)

```python
class Torneo(models.Model):
    """Competiciones y torneos"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    categoria = models.CharField(max_length=50)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('programado', 'Programado'),
            ('en_curso', 'En Curso'),
            ('finalizado', 'Finalizado'),
        ],
        default='programado'
    )
    imagen = models.ImageField(upload_to='torneos/', blank=True, null=True)
```

---

## Sistema de Autenticación

### Autenticación con Cédula

El sistema utiliza la **cédula** como identificador único en lugar del username tradicional.

#### Configuración (settings.py)

```python
AUTH_USER_MODEL = 'users.Usuario'
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'core:dashboard_by_role'
LOGOUT_REDIRECT_URL = 'core:home'
```

### Formulario de Login

```python
class LoginCedulaForm(AuthenticationForm):
    """Formulario de login con cédula"""
    username = forms.CharField(
        label='Cédula',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Cédula'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
```

### Vista de Login

```python
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginCedulaForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:dashboard_by_role')
```

### Proceso de Login

1. Usuario ingresa cédula y contraseña
2. Sistema valida credenciales usando `authenticate()`
3. Si es válido, crea sesión con `login()`
4. Redirige al dashboard según rol del usuario

### Formulario de Registro

```python
class CustomUsuarioCreationForm(UserCreationForm):
    """Formulario de registro - Solo Jugador/Árbitro"""
    ROLE_CHOICES = (
        ('es_jugador', 'Jugador'),
        ('es_arbitro', 'Árbitro'),
        # NO incluye 'es_admin_aso' - seguridad
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de usuario",
        required=True
    )
```

### Proceso de Registro

1. Usuario completa formulario con datos personales
2. Selecciona rol: Jugador o Árbitro
3. Sistema valida datos (unicidad de cédula/email)
4. Crea usuario con rol seleccionado
5. Redirige a login para autenticarse

---

## Roles y Permisos

### Tipos de Usuarios

El sistema maneja **4 niveles** de usuarios:

#### 1. Usuario Anónimo

- **Permisos:** Solo lectura
- **Acceso:** Página principal, noticias públicas
- **Restricciones:** No puede acceder a dashboards

#### 2. Jugador (`es_jugador=True`)

- **Permisos:** Gestión de perfil propio
- **Acceso:**
  - Dashboard de jugador
  - Ver torneos
  - Ver ranking
  - Editar perfil
- **Restricciones:** No puede crear contenido

#### 3. Árbitro (`es_arbitro=True`)

- **Permisos:** Gestión de perfil + arbitraje
- **Acceso:**
  - Dashboard de árbitro
  - Ver partidos asignados
  - Registrar resultados
  - Editar perfil
- **Restricciones:** No puede gestionar usuarios

#### 4. Administrador Regular (`es_admin_aso=True, is_staff=True, is_superuser=False`)

- **Permisos:** Gestión de contenido
- **Acceso:**
  - Dashboard de administrador
  - Crear/editar noticias
  - Gestionar torneos
  - Gestionar canchas
  - Ver jugadores y árbitros
  - Acceso limitado a Django Admin
- **Restricciones:** **NO puede crear más administradores**

#### 5. Superusuario (`is_superuser=True, is_staff=True, es_admin_aso=True`)

- **Permisos:** Control total del sistema
- **Acceso:**
  - Todo lo de Administrador Regular
  - **Gestión de administradores** (promover/degradar)
  - Acceso completo a Django Admin
  - Configuración del sistema
- **Creación:** Solo mediante `python manage.py createsuperuser`

### Matriz de Permisos

| Funcionalidad | Anónimo | Jugador | Árbitro | Admin | Superuser |
|---------------|---------|---------|---------|-------|-----------|
| Ver home | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver noticias | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editar perfil | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ver dashboard | ❌ | ✅ | ✅ | ✅ | ✅ |
| Crear noticias | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gestionar torneos | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gestionar canchas | ❌ | ❌ | ❌ | ✅ | ✅ |
| Arbitrar partidos | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Gestionar admins** | ❌ | ❌ | ❌ | ❌ | ✅ |
| Django Admin | ❌ | ❌ | ❌ | Limitado | ✅ |

### Decoradores de Permisos

```python
# Requiere autenticación
@login_required
def perfil_usuario(request):
    pass

# Requiere ser superusuario
@user_passes_test(lambda u: u.is_superuser, login_url='core:home')
def admin_management(request):
    pass

# Requiere ser admin (regular o super)
@user_passes_test(lambda u: u.es_admin_aso, login_url='core:home')
def admin_dashboard(request):
    pass
```

---

## Módulos del Sistema

### 1. Módulo de Usuarios (users/)

#### Funcionalidades

- ✅ Registro de usuarios (Jugador/Árbitro)
- ✅ Login con cédula
- ✅ Gestión de perfil
- ✅ **Gestión de administradores** (solo superusers)

#### Vistas Principales

**`register_user(request)`**

- Template: `users/register.html`
- Permite registro como Jugador o Árbitro
- Valida unicidad de cédula y email

**`CustomLoginView`**

- Template: `users/login.html`
- Autenticación con cédula
- Redirige a dashboard según rol

**`perfil_usuario(request)`**

- Template: `users/perfil.html`
- Edición de perfil del usuario autenticado
- Requiere login

**`admin_management(request)`** ⭐

- Template: `users/admin_management.html`
- **Solo superusuarios**
- Lista superusers y admins regulares
- Buscador de usuarios para promover

**`promote_to_admin(request, user_id)`** ⭐

- Promueve usuario a administrador
- Establece `es_admin_aso=True` y `is_staff=True`
- **Solo superusuarios**

**`demote_from_admin(request, user_id)`** ⭐

- Remueve privilegios de admin
- No permite degradar superusuarios
- **Solo superusuarios**

### 2. Módulo Core (core/)

#### Funcionalidades

- ✅ Página principal
- ✅ Dashboards diferenciados por rol
- ✅ Gestión de Hero
- ✅ Enrutamiento inteligente

#### Vistas Principales

**`home(request)`**

- Template: `home.html`
- Muestra hero activo
- Noticias destacadas
- Próximos torneos

**`dashboard_by_role(request)`**

- Redirige al dashboard apropiado según rol:
  - Jugador → `panel_jugador.html`
  - Árbitro → `panel_arbitro.html`
  - Admin → `panel_admin.html`

**`admin_dashboard(request)`**

- Template: `users/panel_admin.html`
- Métricas del sistema
- Accesos rápidos a gestión

### 3. Módulo de Competiciones (competitions/)

#### Funcionalidades

- ✅ Gestión de torneos
- ✅ Registro de partidos
- ✅ Seguimiento de resultados
- ✅ Rankings

#### Modelos

**Torneo**

- Información del torneo
- Fechas y categoría
- Estado (programado/en curso/finalizado)

**Partido**

- Enfrentamiento entre equipos
- Resultado y puntuación
- Árbitro asignado

### 4. Módulo de Instalaciones (facilities/)

#### Funcionalidades

- ✅ Registro de canchas
- ✅ Gestión de disponibilidad
- ✅ Información de ubicación

#### Modelo Cancha

- Nombre y ubicación
- Tipo (indoor/outdoor)
- Estado de disponibilidad
- Imagen

### 5. Módulo de Blog (blog/)

#### Funcionalidades

- ✅ Publicación de noticias
- ✅ Gestión de comunicados
- ✅ Noticias destacadas

#### Modelo Noticia

- Título y contenido
- Autor (ForeignKey a Usuario)
- Imagen destacada
- Fecha de publicación
- Flag de destacada

---

## Flujos de Trabajo

### Flujo de Registro de Usuario

```mermaid
graph TD
    A[Usuario visita /register/] --> B[Completa formulario]
    B --> C{Datos válidos?}
    C -->|No| B
    C -->|Sí| D[Selecciona rol: Jugador/Árbitro]
    D --> E[Sistema crea usuario]
    E --> F[Redirige a login]
    F --> G[Usuario inicia sesión]
    G --> H[Redirige a dashboard]
```

### Flujo de Gestión de Administradores

```mermaid
graph TD
    A[Superuser accede a /admin-management/] --> B[Ve lista de admins]
    B --> C[Busca usuario]
    C --> D{Usuario encontrado?}
    D -->|No| C
    D -->|Sí| E[Click en Promover]
    E --> F[Confirmación]
    F --> G{Confirma?}
    G -->|No| B
    G -->|Sí| H[Sistema establece es_admin_aso=True]
    H --> I[Usuario ahora es admin]
    I --> J[Puede acceder a panel admin]
    J --> K{Puede gestionar admins?}
    K -->|No| L[Admin regular - sin acceso]
    K -->|Sí| M[Solo si es superuser]
```

### Flujo de Creación de Torneo

```mermaid
graph TD
    A[Admin accede a panel] --> B[Click en Crear Torneo]
    B --> C[Completa formulario]
    C --> D{Datos válidos?}
    D -->|No| C
    D -->|Sí| E[Sistema crea torneo]
    E --> F[Estado: Programado]
    F --> G[Visible en lista de torneos]
```

---

## API y Endpoints

### URLs de Autenticación (users/)

| URL | Vista | Método | Permisos | Descripción |
|-----|-------|--------|----------|-------------|
| `/users/login/` | `CustomLoginView` | GET, POST | Público | Login con cédula |
| `/users/logout/` | `LogoutView` | POST | Autenticado | Cerrar sesión |
| `/users/register/` | `register_user` | GET, POST | Público | Registro de usuario |
| `/users/perfil/` | `perfil_usuario` | GET, POST | Autenticado | Ver/editar perfil |
| `/users/admin-management/` | `admin_management` | GET | Superuser | Panel de gestión de admins |
| `/users/admin-management/promote/<id>/` | `promote_to_admin` | POST | Superuser | Promover a admin |
| `/users/admin-management/demote/<id>/` | `demote_from_admin` | POST | Superuser | Degradar admin |

### URLs de Core (core/)

| URL | Vista | Método | Permisos | Descripción |
|-----|-------|--------|----------|-------------|
| `/` | `home` | GET | Público | Página principal |
| `/dashboard/` | `dashboard_by_role` | GET | Autenticado | Dashboard según rol |
| `/admin/dashboard/` | `admin_dashboard` | GET | Admin | Panel de administrador |
| `/admin/hero/edit/` | `admin_edit_hero` | GET, POST | Admin | Editar hero |

### URLs de Blog (blog/)

| URL | Vista | Método | Permisos | Descripción |
|-----|-------|--------|----------|-------------|
| `/noticias/` | `noticias_list` | GET | Público | Lista de noticias |
| `/noticias/<id>/` | `noticia_detail` | GET | Público | Detalle de noticia |
| `/admin/noticias/` | `admin_noticias_list` | GET | Admin | Gestión de noticias |
| `/admin/noticias/crear/` | `admin_create_noticia` | GET, POST | Admin | Crear noticia |

---

## Frontend y Templates

### Sistema de Templates

#### Template Base (base.html)

Estructura común para todas las páginas:

```html
<!DOCTYPE html>
<html lang="es" data-bs-theme="auto">
<head>
    <!-- Meta tags, CSS -->
    <link href="bootstrap.min.css" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
</head>
<body>
    <!-- SVG Icons para tema -->
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none">
        <!-- Iconos de sol, luna, etc. -->
    </svg>
    
    <!-- Navbar -->
    <nav class="navbar">
        <!-- Logo, links, selector de tema -->
    </nav>
    
    <!-- Contenido -->
    {% block content %}{% endblock %}
    
    <!-- Footer -->
    <footer>
        <!-- Copyright, links -->
    </footer>
    
    <!-- Scripts -->
    <script src="bootstrap.bundle.min.js"></script>
    <script src="main.js"></script>
</body>
</html>
```

### Modo Oscuro/Claro

#### Implementación JavaScript (main.js)

```javascript
(() => {
  "use strict";
  
  const storedTheme = localStorage.getItem("theme");
  
  const getPreferredTheme = () => {
    if (storedTheme) return storedTheme;
    return window.matchMedia("(prefers-color-scheme: dark)").matches 
      ? "dark" : "light";
  };
  
  const setTheme = function (theme) {
    let themeToApply = theme;
    
    if (theme === "auto" && 
        window.matchMedia("(prefers-color-scheme: dark)").matches) {
      themeToApply = "dark";
    } else if (theme === "auto") {
      themeToApply = "light";
    }
    
    // Bootstrap theme
    document.documentElement.setAttribute("data-bs-theme", themeToApply);
    
    // Custom dark mode class
    if (themeToApply === "dark") {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  };
  
  // Aplicar tema al cargar
  setTheme(getPreferredTheme());
  
  // Event listeners para botones de tema
  document.querySelectorAll('[data-bs-theme-value]').forEach(button => {
    button.addEventListener('click', () => {
      const theme = button.getAttribute('data-bs-theme-value');
      localStorage.setItem('theme', theme);
      setTheme(theme);
    });
  });
})();
```

#### Selector de Tema (base.html)

```html
<li class="nav-item dropdown">
  <button class="btn btn-link nav-link dropdown-toggle" 
          id="bd-theme" 
          data-bs-toggle="dropdown">
    <svg class="bi theme-icon-active">
      <use href="#circle-half"></use>
    </svg>
    <span class="d-lg-none ms-2">Cambiar Tema</span>
  </button>
  
  <ul class="dropdown-menu dropdown-menu-end">
    <li>
      <button class="dropdown-item" data-bs-theme-value="light">
        <svg class="bi me-2"><use href="#sun-fill"></use></svg>
        Claro
      </button>
    </li>
    <li>
      <button class="dropdown-item" data-bs-theme-value="dark">
        <svg class="bi me-2"><use href="#moon-stars-fill"></use></svg>
        Oscuro
      </button>
    </li>
    <li>
      <button class="dropdown-item active" data-bs-theme-value="auto">
        <svg class="bi me-2"><use href="#circle-half"></use></svg>
        Sistema
      </button>
    </li>
  </ul>
</li>
```

### Diseño Responsive

#### Breakpoints de Bootstrap

```css
/* Mobile First */
.col-12          /* Móvil: 100% ancho */
.col-sm-6        /* Tablet: 50% ancho (≥576px) */
.col-md-4        /* Desktop: 33% ancho (≥768px) */
.col-lg-3        /* Large: 25% ancho (≥992px) */
.col-xl-2        /* XL: 16.6% ancho (≥1200px) */
```

#### Ejemplo: Formulario de Registro

```html
<div class="row g-3">
  <div class="col-12 col-md-6">
    <!-- Campo de cédula -->
  </div>
  <div class="col-12 col-md-6">
    <!-- Campo de email -->
  </div>
</div>
```

**Comportamiento:**

- **Móvil (< 768px):** Campos en 1 columna (100% ancho)
- **Tablet/Desktop (≥ 768px):** Campos en 2 columnas (50% ancho cada uno)

---

## Tests y Calidad

### Estrategia de Testing

El proyecto implementa **43 tests** organizados en 3 archivos:

#### 1. Tests de Modelos (test_models.py) - 15 tests

**UsuarioManagerTestCase:**

- `test_create_user` - Creación de usuario regular
- `test_create_user_without_cedula` - Validación de cédula obligatoria
- `test_create_superuser` - Creación de superusuario
- `test_create_superuser_with_wrong_flags` - Validación de flags

**UsuarioModelTestCase:**

- `test_str_method` - Método `__str__`
- `test_get_full_name` - Propiedad nombre completo
- `test_get_short_name` - Propiedad nombre corto
- `test_jugador_role` - Asignación de rol jugador
- `test_arbitro_role` - Asignación de rol árbitro
- `test_admin_role` - Asignación de rol admin
- `test_multiple_roles` - Múltiples roles simultáneos
- `test_categoria_jugador_choices` - Validación de categorías
- `test_ranking_default` - Valor por defecto de ranking
- `test_unique_cedula` - Unicidad de cédula
- `test_unique_email` - Unicidad de email

#### 2. Tests de Formularios (test_forms.py) - 11 tests

**LoginCedulaFormTestCase:**

- `test_form_fields` - Campos del formulario
- `test_valid_login` - Login válido

**CustomUsuarioCreationFormTestCase:**

- `test_form_has_role_field` - Campo de rol presente
- `test_role_choices_no_admin` - **Admin NO disponible**
- `test_create_jugador` - Registro como jugador
- `test_create_arbitro` - Registro como árbitro
- `test_password_mismatch` - Validación de contraseñas
- `test_required_fields` - Campos obligatorios
- `test_duplicate_cedula` - Validación de cédula única

**CustomUsuarioChangeFormTestCase:**

- `test_form_includes_all_fields` - Todos los campos presentes
- `test_update_user_info` - Actualización de información

#### 3. Tests de Vistas (test_views.py) - 17 tests

**RegistrationViewTestCase:**

- `test_register_page_loads` - Página carga correctamente
- `test_register_jugador_success` - Registro exitoso como jugador
- `test_register_arbitro_success` - Registro exitoso como árbitro
- `test_cannot_register_as_admin` - **No se puede registrar como admin**

**LoginViewTestCase:**

- `test_login_page_loads` - Página carga correctamente
- `test_login_with_cedula` - Login con cédula
- `test_login_with_wrong_password` - Contraseña incorrecta

**AdminManagementViewTestCase:**

- `test_admin_management_requires_login` - Requiere autenticación
- `test_admin_management_requires_superuser` - **Solo superusuarios**
- `test_superuser_can_view_admin_list` - Superuser ve lista
- `test_promote_user_to_admin` - **Promover a admin**
- `test_demote_admin_to_regular_user` - **Degradar admin**
- `test_cannot_demote_superuser` - **No degradar superuser**
- `test_regular_user_cannot_promote` - Usuario regular no puede promover

**PerfilViewTestCase:**

- `test_perfil_requires_login` - Requiere autenticación
- `test_perfil_loads_for_authenticated_user` - Carga para usuario autenticado

### Ejecución de Tests

#### Opción 1: Script Automatizado

```bash
chmod +x run_tests.sh
./run_tests.sh
```

#### Opción 2: Comandos Manuales

```bash
# Activar entorno virtual
source venv/bin/activate

# Todos los tests de users
python manage.py test users --verbosity=2

# Tests específicos
python manage.py test users.test_models --verbosity=2
python manage.py test users.test_forms --verbosity=2
python manage.py test users.test_views --verbosity=2

# Test individual
python manage.py test users.test_views.AdminManagementViewTestCase.test_promote_user_to_admin
```

### Cobertura de Tests

```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con coverage
coverage run --source='.' manage.py test users

# Ver reporte
coverage report

# Generar HTML
coverage html
```

---

## Configuración y Despliegue

### Variables de Entorno (.env)

```env
# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Base de Datos (desarrollo)
DATABASE_URL=sqlite:///db.sqlite3

# Base de Datos (producción)
DATABASE_URL=postgresql://usuario:password@host:puerto/nombre_db

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

### Configuración de Producción

#### settings.py

```python
# Seguridad
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']

# Base de datos
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:pass@localhost/dbname',
        conn_max_age=600
    )
}

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

### Despliegue con Docker

#### Dockerfile

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
```

#### docker-compose.yml

```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - SECRET_KEY=django-insecure-docker-dev-key
      - DEBUG=True
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/asopadel_barinas
    entrypoint: /app/entrypoint.sh
    
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=asopadel_barinas
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

#### entrypoint.sh

```bash
#!/bin/sh

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
gunicorn asopadel_barinas.wsgi:application --bind 0.0.0.0:8000
```

### Comandos de Despliegue

```bash
# Construir y levantar
docker compose up --build

# Crear superusuario
docker compose exec web python manage.py createsuperuser

# Ver logs
docker compose logs -f web

# Detener
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

---

## Guías de Desarrollo

### Agregar un Nuevo Modelo

1. **Definir el modelo** en `app/models.py`:

```python
class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mi Modelo"
        verbose_name_plural = "Mis Modelos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre
```

2. **Crear migraciones**:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Registrar en admin** (opcional):

```python
# app/admin.py
from django.contrib import admin
from .models import MiModelo

@admin.register(MiModelo)
class MiModeloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']
    search_fields = ['nombre']
```

### Agregar una Nueva Vista

1. **Crear vista** en `app/views.py`:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista(request):
    context = {
        'titulo': 'Mi Vista'
    }
    return render(request, 'app/mi_template.html', context)
```

2. **Agregar URL** en `app/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('mi-ruta/', views.mi_vista, name='mi_vista'),
]
```

3. **Crear template** en `templates/app/mi_template.html`:

```html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container">
    <h1>{{ titulo }}</h1>
    <!-- Contenido -->
</div>
{% endblock %}
```

### Agregar Tests

1. **Crear archivo de tests** `app/test_mi_funcionalidad.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import MiModelo

class MiFuncionalidadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.objeto = MiModelo.objects.create(
            nombre='Test'
        )
    
    def test_mi_funcionalidad(self):
        response = self.client.get(reverse('mi_vista'))
        self.assertEqual(response.status_code, 200)
```

2. **Ejecutar tests**:

```bash
python manage.py test app.test_mi_funcionalidad
```

### Buenas Prácticas

#### Código

- ✅ Usar nombres descriptivos en español para modelos y campos
- ✅ Documentar funciones complejas con docstrings
- ✅ Validar datos en formularios antes de guardar
- ✅ Usar decoradores de permisos en vistas sensibles
- ✅ Mantener vistas pequeñas y enfocadas

#### Base de Datos

- ✅ Crear índices para campos de búsqueda frecuente
- ✅ Usar `select_related()` y `prefetch_related()` para optimizar queries
- ✅ Validar datos con `clean()` en modelos
- ✅ Usar transacciones para operaciones críticas

#### Templates

- ✅ Extender de `base.html` para consistencia
- ✅ Usar bloques de Django para sobrescribir secciones
- ✅ Aplicar clases de Bootstrap para responsive
- ✅ Escapar HTML con `{{ variable|safe }}` solo cuando sea necesario

#### Seguridad

- ✅ Nunca exponer `SECRET_KEY` en código
- ✅ Usar `@login_required` para vistas privadas
- ✅ Validar permisos con `@user_passes_test`
- ✅ Sanitizar inputs de usuario
- ✅ Usar CSRF tokens en formularios

---

## Apéndices

### Comandos Útiles de Django

```bash
# Crear proyecto
django-admin startproject nombre_proyecto

# Crear app
python manage.py startapp nombre_app

# Migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Servidor de desarrollo
python manage.py runserver
python manage.py runserver 0.0.0.0:8000

# Archivos estáticos
python manage.py collectstatic

# Tests
python manage.py test
python manage.py test app.tests.TestCase

# Base de datos
python manage.py dbshell
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
```

### Estructura de Commits

Seguir convención de **Conventional Commits**:

```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
style: cambios de formato (sin afectar código)
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

### Recursos Adicionales

- **Django Documentation:** <https://docs.djangoproject.com/>
- **Bootstrap Documentation:** <https://getbootstrap.com/docs/>
- **Django Testing:** <https://docs.djangoproject.com/en/stable/topics/testing/>
- **PostgreSQL:** <https://www.postgresql.org/docs/>

---

## Conclusión

Este documento proporciona una visión completa del sistema ASOPADEL BARINAS, desde su arquitectura hasta los detalles de implementación. Para cualquier duda o contribución, consultar con el equipo de desarrollo.

**Última actualización:** 2025-11-24  
**Versión del documento:** 1.0  
**Mantenido por:** Equipo de Desarrollo ASOPADEL
